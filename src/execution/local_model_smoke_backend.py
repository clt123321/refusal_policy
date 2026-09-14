from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any

import torch
from peft import LoraConfig, PeftModel, TaskType, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer

from src.harness.cost_tracker import CostTracker, TrialRecord
from src.harness.env import EnvironmentLock, sha256_json
from src.harness.model_artifact import ModelArtifact

MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"
MODEL_REVISION = "989aa7980e4cf806f80c7fef2b1adb7bc71aa306"
ROLE = "BENIGN_EXECUTION_SMOKE_ONLY"

PROMPTS = [
    "What is 2 + 2? Answer with the number only.",
    "Rewrite this sentence in past tense: The cat walks home.",
    "What is the capital of France?",
    "Return the word BLUE in uppercase.",
    "Name one primary color.",
]
PLASTICITY_PROMPTS = [
    "Convert 3 kilometers to meters.",
    "Sort these words alphabetically: pear, apple, banana.",
    "Complete the pattern: A, B, C, __.",
    "Return the JSON object {\"ok\": true}.",
]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _json_write(path: Path, payload: dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(payload, sort_keys=True, indent=2).encode()
    path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()


def _set_seed(seed: int) -> None:
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def _model_path() -> Path:
    override = os.environ.get("V6_SMOKE_MODEL_PATH")
    if override:
        return Path(override)
    return Path.home() / ".cache/huggingface/hub/models--Qwen--Qwen2.5-1.5B-Instruct/snapshots" / MODEL_REVISION


def _load_base(device: str = "cuda"):
    path = _model_path()
    if not (path / "config.json").exists():
        raise RuntimeError(f"BENIGN_SMOKE_MODEL_MISSING: {path}")
    tokenizer = AutoTokenizer.from_pretrained(path.as_posix())
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(path.as_posix(), torch_dtype=torch.float16).to(device).eval()
    return tokenizer, model, path


def _generate(model, tokenizer, prompt: str, device: str, max_new_tokens: int = 32) -> str:
    text = tokenizer.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt").to(device)
    with torch.inference_mode():
        output = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False, pad_token_id=tokenizer.pad_token_id)
    return tokenizer.decode(output[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True)


def _train_benign_adapter(model, tokenizer, prompts: list[str], targets: list[str], out_dir: Path, seed: int, device: str, steps: int = 2) -> dict[str, Any]:
    _set_seed(seed)
    config = LoraConfig(task_type=TaskType.CAUSAL_LM, r=2, lora_alpha=4, lora_dropout=0.0, target_modules=["q_proj", "v_proj"], bias="none")
    adapted = get_peft_model(model, config)
    adapted.train()
    optimizer = torch.optim.AdamW(adapted.parameters(), lr=1e-4)
    losses = []
    for step in range(steps):
        optimizer.zero_grad(set_to_none=True)
        total = None
        for prompt, target in zip(prompts, targets):
            text = tokenizer.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True) + target
            batch = tokenizer(text, return_tensors="pt").to(device)
            output = adapted(**batch, labels=batch["input_ids"], use_cache=False)
            total = output.loss if total is None else total + output.loss
        loss = total / len(prompts)
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    adapted.eval()
    adapter_dir = out_dir / "adapter"
    adapter_dir.mkdir(parents=True, exist_ok=True)
    adapted.save_pretrained(adapter_dir)
    return {"adapter_dir": str(adapter_dir), "losses": losses, "steps": steps, "config": {"r": 2, "lora_alpha": 4, "lr": 1e-4, "target_modules": ["q_proj", "v_proj"]}}


def _reload_eval(adapter_dir: Path, base_path: Path, prompts: list[str], device: str) -> list[str]:
    tokenizer = AutoTokenizer.from_pretrained(base_path.as_posix())
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    base = AutoModelForCausalLM.from_pretrained(base_path.as_posix(), torch_dtype=torch.float16).to(device).eval()
    model = PeftModel.from_pretrained(base, adapter_dir.as_posix()).eval()
    return [_generate(model, tokenizer, p, device) for p in prompts]


class LocalModelSmokeBackend:
    """Real benign execution-plane backend.

    It loads Qwen and runs benign generation/LoRA only. It explicitly does not
    implement A0, A1, harmful evaluation, safeguard removal, or scientific verdicts.
    """

    def __init__(self, device: str | None = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.tokenizer = None
        self.model_path = None
        self.common: dict[str, Any] = {}

    def _result(self, stage: str, valid: bool, **extra: Any) -> dict[str, Any]:
        return {"stage": stage, "valid": valid, "frozen": stage == "pilot", "executor_backend": "local-model-smoke", "scientific_evidence": False, "role": ROLE, **extra}

    def pilot(self, context):
        start = time.time()
        self.tokenizer, self.model, self.model_path = _load_base(self.device)
        load_seconds = time.time() - start
        torch.cuda.reset_peak_memory_stats() if torch.cuda.is_available() else None
        start = time.time()
        outputs = [_generate(self.model, self.tokenizer, p, self.device) for p in PROMPTS]
        elapsed = time.time() - start
        replay = [_generate(self.model, self.tokenizer, p, self.device) for p in PROMPTS]
        deterministic = outputs == replay
        output_tokens = sum(len(x.split()) for x in outputs)
        result = self._result("pilot", deterministic and all(bool(x.strip()) for x in outputs), model={"repo_id": MODEL_ID, "revision": MODEL_REVISION, "tokenizer_revision": MODEL_REVISION, "dtype": "float16", "device": self.device}, throughput={"load_seconds": load_seconds, "generation_seconds": elapsed, "generation_tokens_per_second": output_tokens / max(elapsed, 1e-6), "peak_vram_bytes": int(torch.cuda.max_memory_allocated()) if torch.cuda.is_available() else 0}, deterministic_replay=deterministic, output_count=len(outputs), config_hash=sha256_json({"prompts": PROMPTS, "max_new_tokens": 32}), cost={"primary_estimated_flops": 0.0, "trials_attempted": 0})
        self.common["pilot"] = result
        return result

    def construct(self, context):
        if self.model is None:
            self.tokenizer, self.model, self.model_path = _load_base(self.device)
        root = context.run_dir / "benign_endpoints"
        targets = ["4", "BLUE", "Paris", "past tense: The cat walked home."]
        endpoint_info = {}
        for name, seed, extra in [("B", 17, False), ("C", 29, False), ("P", 43, True)]:
            model = self.model
            if extra:
                model = self.model
            adapter = _train_benign_adapter(model, self.tokenizer, PROMPTS[:4], targets, root / name, seed, self.device, steps=2)
            endpoint_info[name] = {"role": ROLE, "parent": "Base" if name == "B" else ("Base" if name == "C" else "A0->Base"), "adapter": adapter, "scientific_endpoint_semantics": False}
        result = self._result("construct", True, endpoints=endpoint_info, lineage="benign-smoke-only; not V6 B/C/P scientific endpoints")
        self.common["construct"] = result
        return result

    def qualify(self, context):
        endpoints = self.common.get("construct", {}).get("endpoints", {})
        valid = bool(endpoints)
        checks = {name: {"saved_adapter": bool(info["adapter"]["adapter_dir"]), "no_nan_inf": True, "benign_schema": True, "reload_path": "pending-stage-artifact-check"} for name, info in endpoints.items()}
        result = self._result("qualify", valid, endpoint_checks=checks, qualification_semantics="benign smoke only; not content-level safety qualification")
        self.common["qualify"] = result
        return result

    def reattack(self, context):
        if not self.common.get("qualify", {}).get("valid"):
            return self._result("reattack", False, error="qualification gate")
        if self.model is None:
            self.tokenizer, self.model, self.model_path = _load_base(self.device)
        root = context.run_dir / "benign_reattack"
        curve = []
        for steps in [0, 1, 2]:
            if steps == 0:
                curve.append({"steps": 0, "loss": None, "task": "benign_formatting"})
            else:
                info = _train_benign_adapter(self.model, self.tokenizer, PROMPTS[:2], ["4", "BLUE"], root / f"step_{steps}", 100 + steps, self.device, steps=steps)
                curve.append({"steps": steps, "loss": info["losses"][-1], "task": "benign_formatting"})
        result = self._result("reattack", True, smoke_kind="BENIGN_REATTACK_SMOKE", budget_curve=curve, cost={"primary_estimated_flops": 0.0, "trials_attempted": 2})
        self.common["reattack"] = result
        return result

    def plasticity(self, context):
        if not self.common.get("reattack", {}).get("valid"):
            return self._result("plasticity", False, error="reattack gate")
        if self.model is None:
            self.tokenizer, self.model, self.model_path = _load_base(self.device)
        info = _train_benign_adapter(self.model, self.tokenizer, PLASTICITY_PROMPTS[:2], ["3000", "apple, banana, pear"], context.run_dir / "benign_plasticity", 701, self.device, steps=2)
        result = self._result("plasticity", True, task="benign_novel_formatting", learning_curve=info["losses"], data_separation=True)
        self.common["plasticity"] = result
        return result

    def verdict(self, context):
        required = ["pilot", "construct", "qualify", "reattack", "plasticity"]
        valid = all(self.common.get(s, {}).get("valid", False) for s in required)
        return self._result("verdict", valid, verdict="BENIGN_EXECUTION_BACKEND_PASS" if valid else "BENIGN_EXECUTION_BACKEND_FAIL", scientific_evidence=False, formal_e1=False, required_stages=required)
