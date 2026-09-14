from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

import torch
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _hash_json(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _require_frozen(config: dict[str, Any]) -> None:
    data = config.get("data", {})
    if not data.get("path") or not data.get("file_sha256") or not data.get("ids_sha256"):
        raise ValueError("REPAIR_CONFIG_NOT_FROZEN: D_repair path/file_sha256/ids_sha256 required")
    if config.get("objective", {}).get("status", "").startswith("PENDING"):
        raise ValueError("REPAIR_CONFIG_NOT_FROZEN: objective")
    if config.get("trainable", {}).get("status", "").startswith("ENGINEERING_DEFAULT"):
        raise ValueError("REPAIR_CONFIG_NOT_FROZEN: trainable parameterization")
    if config.get("optimizer", {}).get("status", "").startswith("ENGINEERING_DEFAULT"):
        raise ValueError("REPAIR_CONFIG_NOT_FROZEN: optimizer")
    if config.get("schedule", {}).get("status", "").startswith("PENDING"):
        raise ValueError("REPAIR_CONFIG_NOT_FROZEN: schedule")


def load_jsonl_repair_data(path: Path) -> list[dict[str, Any]]:
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    if not rows:
        raise ValueError("D_repair is empty")
    for row in rows:
        if not isinstance(row.get("prompt"), str) or not isinstance(row.get("target"), str):
            raise ValueError("D_repair rows require prompt and target strings")
    return rows


def run_repair(config_path: Path, parent_model_path: Path, output_dir: Path, device: str = "cuda") -> dict[str, Any]:
    config = json.loads(config_path.read_text())
    _require_frozen(config)
    data_path = Path(config["data"]["path"])
    if _sha256(data_path) != config["data"]["file_sha256"]:
        raise ValueError("D_REPAIR_HASH_MISMATCH")
    rows = load_jsonl_repair_data(data_path)
    seed = int(config["seed"])
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    started = time.time()
    tokenizer = AutoTokenizer.from_pretrained(parent_model_path.as_posix())
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(parent_model_path.as_posix(), torch_dtype=torch.float16).to(device)
    lora = config["trainable"]
    adapter_config = LoraConfig(task_type="CAUSAL_LM", r=lora["rank"], lora_alpha=lora["alpha"], lora_dropout=lora["dropout"], target_modules=lora["target_modules"], bias="none")
    model = get_peft_model(model, adapter_config)
    model.train()
    opt_cfg = config["optimizer"]
    optimizer = torch.optim.AdamW(model.parameters(), lr=opt_cfg["learning_rate"], weight_decay=opt_cfg["weight_decay"], betas=tuple(opt_cfg["betas"]))
    losses = []
    for step in range(1, int(config["schedule"]["steps"]) + 1):
        optimizer.zero_grad(set_to_none=True)
        total = None
        for row in rows:
            prompt = tokenizer.apply_chat_template([{"role": "user", "content": row["prompt"]}], tokenize=False, add_generation_prompt=True)
            batch = tokenizer(prompt + row["target"], return_tensors="pt").to(device)
            loss = model(**batch, labels=batch["input_ids"], use_cache=False).loss
            total = loss if total is None else total + loss
        loss = total / len(rows)
        loss.backward(); optimizer.step(); losses.append(float(loss.detach().cpu()))
    model.eval()
    output_dir.mkdir(parents=True, exist_ok=True)
    adapter_dir = output_dir / "adapter"
    model.save_pretrained(adapter_dir)
    (output_dir / "tokenizer").mkdir(exist_ok=True)
    tokenizer.save_pretrained(output_dir / "tokenizer")
    elapsed = time.time() - started
    result = {"status": "SUCCEEDED", "artifact_role": "V6_REPAIR_CHECKPOINT", "parent_model_path": str(parent_model_path), "parent_config_hash": _hash_json(config["model"]), "config_sha256": _sha256(config_path), "data_sha256": _sha256(data_path), "seed": seed, "steps": config["schedule"]["steps"], "tokens": sum(len(r["prompt"].split()) + len(r["target"].split()) for r in rows) * config["schedule"]["steps"], "losses": losses, "wall_seconds": elapsed, "adapter_dir": str(adapter_dir), "lineage": config["lineage"]}
    (output_dir / "repair_result.json").write_text(json.dumps(result, indent=2))
    return result
