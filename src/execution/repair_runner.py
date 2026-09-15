from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import time
from pathlib import Path
from typing import Any


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _hash_json(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def _full_sha(value: str, field: str) -> None:
    if len(value) != 40 or any(c not in "0123456789abcdef" for c in value.lower()):
        raise ValueError(f"{field} must be a full 40-character git SHA")


def verify_execution_checkout(repo: Path, execution_sha: str) -> None:
    """Require a clean, traceable checkout; the commit need not be on GitHub."""
    _full_sha(execution_sha, "execution_sha")
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, check=True,
        capture_output=True, text=True,
    ).stdout.strip()
    dirty = subprocess.run(
        ["git", "status", "--porcelain"], cwd=repo, check=True,
        capture_output=True, text=True,
    ).stdout.strip()
    if head != execution_sha or dirty:
        raise ValueError("EXECUTION_CHECKOUT_NOT_CLEAN_OR_SHA_MISMATCH")


def _require_executable(config: dict[str, Any]) -> None:
    mode = config.get("mode")
    if mode not in {"DEV", "FORMAL"}:
        raise ValueError("REPAIR_CONFIG_NOT_EXECUTABLE: mode must be DEV or FORMAL")
    data = config.get("data", {})
    if not data.get("path") or not data.get("file_sha256") or not data.get("ids_sha256"):
        raise ValueError("REPAIR_CONFIG_NOT_EXECUTABLE: D_repair path/file_sha256/ids_sha256 required")
    required_status = "FROZEN" if mode == "FORMAL" else "DEV_LOCKED"
    for section in ("objective", "trainable", "optimizer", "schedule"):
        if config.get(section, {}).get("status") != required_status:
            raise ValueError(f"REPAIR_CONFIG_NOT_EXECUTABLE: {section}.status must be {required_status}")
    if mode == "FORMAL" and config.get("scientific_evidence") is not True:
        raise ValueError("REPAIR_CONFIG_NOT_EXECUTABLE: FORMAL scientific_evidence must be true")
    if mode == "DEV" and config.get("scientific_evidence") is not False:
        raise ValueError("REPAIR_CONFIG_NOT_EXECUTABLE: DEV scientific_evidence must be false")
    schedule = config["schedule"]
    steps = int(schedule.get("steps", 0))
    checkpoints = list(schedule.get("checkpoint_steps", []))
    if steps < 1 or int(schedule.get("batch_size", 0)) < 1 or int(schedule.get("gradient_accumulation_steps", 0)) < 1:
        raise ValueError("REPAIR_CONFIG_NOT_EXECUTABLE: positive steps/batch/accumulation required")
    if not checkpoints or checkpoints != sorted(set(checkpoints)) or checkpoints[0] < 0 or checkpoints[-1] != steps:
        raise ValueError("REPAIR_CONFIG_NOT_EXECUTABLE: checkpoint_steps must be sorted, unique and end at steps")
    lineage = config.get("lineage", {})
    if not lineage.get("parent_artifact_id") or lineage.get("arm") not in {"C", "P", "DEV"}:
        raise ValueError("REPAIR_CONFIG_NOT_EXECUTABLE: lineage parent_artifact_id and arm required")


def load_jsonl_repair_data(path: Path) -> list[dict[str, Any]]:
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    if not rows:
        raise ValueError("D_repair is empty")
    for row in rows:
        if not isinstance(row.get("id"), str):
            raise ValueError("D_repair rows require stable string id")
        if not isinstance(row.get("prompt"), str) or not isinstance(row.get("target"), str):
            raise ValueError("D_repair rows require prompt and target strings")
    if len({row["id"] for row in rows}) != len(rows):
        raise ValueError("D_repair row ids must be unique")
    return rows


def _load_ml_runtime():
    try:
        import torch
        from peft import LoraConfig, get_peft_model
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as exc:
        raise RuntimeError("REPAIR_RUNTIME_DEPENDENCY_MISSING: torch/transformers/peft") from exc
    return torch, LoraConfig, get_peft_model, AutoModelForCausalLM, AutoTokenizer


def _save_checkpoint(model, output_dir: Path, step: int) -> str:
    adapter_dir = output_dir / "checkpoints" / f"step_{step:06d}" / "adapter"
    adapter_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(adapter_dir)
    return str(adapter_dir)


def run_repair(
    config_path: Path,
    parent_model_path: Path,
    output_dir: Path,
    device: str = "cuda",
    *,
    execution_sha: str,
    task_id: str,
    run_id: str,
    attempt_id: str,
) -> dict[str, Any]:
    config = json.loads(config_path.read_text())
    _require_executable(config)
    data_path = Path(config["data"]["path"])
    if _sha256(data_path) != config["data"]["file_sha256"]:
        raise ValueError("D_REPAIR_HASH_MISMATCH")
    rows = load_jsonl_repair_data(data_path)
    actual_ids_hash = _hash_json([row["id"] for row in rows])
    if actual_ids_hash != config["data"]["ids_sha256"]:
        raise ValueError("D_REPAIR_IDS_HASH_MISMATCH")
    _full_sha(execution_sha, "execution_sha")
    identity = {
        "experiment_id": "V6.E1", "task_id": task_id, "run_id": run_id,
        "attempt_id": attempt_id, "execution_sha": execution_sha,
        "config_sha256": _sha256(config_path), "data_sha256": _sha256(data_path),
        "parent_artifact_id": config["lineage"]["parent_artifact_id"],
    }
    identity_hash = _hash_json(identity)
    prior_result = output_dir / "repair_result.json"
    if prior_result.exists():
        prior = json.loads(prior_result.read_text())
        if prior.get("run_identity_sha256") == identity_hash:
            return prior
        raise ValueError("OUTPUT_DIR_IDENTITY_COLLISION: use a new attempt_id/output directory")
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError("OUTPUT_DIR_NOT_EMPTY: use a new attempt_id/output directory")

    torch, LoraConfig, get_peft_model, AutoModelForCausalLM, AutoTokenizer = _load_ml_runtime()
    seed = int(config["seed"])
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    started = time.time()
    tokenizer = AutoTokenizer.from_pretrained(parent_model_path.as_posix())
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    dtype = torch.float16 if config["model"].get("dtype") == "float16" else torch.float32
    model = AutoModelForCausalLM.from_pretrained(parent_model_path.as_posix(), torch_dtype=dtype).to(device)
    lora = config["trainable"]
    adapter_config = LoraConfig(
        task_type="CAUSAL_LM", r=lora["rank"], lora_alpha=lora["alpha"],
        lora_dropout=lora["dropout"], target_modules=lora["target_modules"], bias="none",
    )
    model = get_peft_model(model, adapter_config)
    model.train()
    opt_cfg = config["optimizer"]
    optimizer = torch.optim.AdamW(
        model.parameters(), lr=opt_cfg["learning_rate"], weight_decay=opt_cfg["weight_decay"],
        betas=tuple(opt_cfg["betas"]),
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_steps = set(config["schedule"]["checkpoint_steps"])
    checkpoint_artifacts: dict[str, str] = {}
    if 0 in checkpoint_steps:
        checkpoint_artifacts["0"] = _save_checkpoint(model, output_dir, 0)
    batch_size = int(config["schedule"]["batch_size"])
    accumulation = int(config["schedule"]["gradient_accumulation_steps"])
    losses: list[float] = []
    training_tokens = 0
    for step in range(1, int(config["schedule"]["steps"]) + 1):
        optimizer.zero_grad(set_to_none=True)
        step_loss = 0.0
        for micro in range(accumulation):
            offset = ((step - 1) * accumulation + micro) * batch_size
            batch_rows = [rows[(offset + index) % len(rows)] for index in range(batch_size)]
            micro_total = None
            for row in batch_rows:
                prompt = tokenizer.apply_chat_template(
                    [{"role": "user", "content": row["prompt"]}], tokenize=False,
                    add_generation_prompt=True,
                )
                full = tokenizer(prompt + row["target"], return_tensors="pt", add_special_tokens=False).to(device)
                prefix = tokenizer(prompt, return_tensors="pt", add_special_tokens=False)
                labels = full["input_ids"].clone()
                labels[:, :prefix["input_ids"].shape[1]] = -100
                loss = model(**full, labels=labels, use_cache=False).loss
                micro_total = loss if micro_total is None else micro_total + loss
                training_tokens += int(full["input_ids"].numel())
            micro_loss = micro_total / len(batch_rows) / accumulation
            micro_loss.backward()
            step_loss += float(micro_loss.detach().cpu())
        if not math.isfinite(step_loss):
            raise RuntimeError("NONFINITE_REPAIR_LOSS")
        optimizer.step()
        losses.append(step_loss)
        if step in checkpoint_steps:
            checkpoint_artifacts[str(step)] = _save_checkpoint(model, output_dir, step)
    model.eval()
    adapter_dir = output_dir / "adapter"
    model.save_pretrained(adapter_dir)
    tokenizer_dir = output_dir / "tokenizer"
    tokenizer.save_pretrained(tokenizer_dir)
    elapsed = time.time() - started
    result = {
        "status": "SUCCEEDED", "execution_completed": True,
        "scientific_evidence": bool(config["scientific_evidence"]),
        "artifact_role": "V6_REPAIR_CHECKPOINT", **identity,
        "run_identity_sha256": identity_hash,
        "parent_model_path": str(parent_model_path),
        "parent_config_hash": _hash_json(config["model"]),
        "seed": seed, "steps": config["schedule"]["steps"],
        "training_tokens": training_tokens, "losses": losses,
        "wall_seconds": elapsed, "adapter_dir": str(adapter_dir),
        "checkpoint_artifacts": checkpoint_artifacts, "lineage": config["lineage"],
    }
    prior_result.write_text(json.dumps(result, sort_keys=True, indent=2))
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a traceable V6 repair task")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--parent-model", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--execution-sha", required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--attempt-id", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        verify_execution_checkout(args.repo, args.execution_sha)
        result = run_repair(
            args.config, args.parent_model, args.output, args.device,
            execution_sha=args.execution_sha, task_id=args.task_id,
            run_id=args.run_id, attempt_id=args.attempt_id,
        )
        print(json.dumps(result, sort_keys=True, indent=2))
        return 0
    except Exception as exc:
        args.output.mkdir(parents=True, exist_ok=True)
        failure = {
            "status": "FAILED", "execution_completed": True,
            "scientific_evidence": False, "attempt_charged": True,
            "task_id": args.task_id, "run_id": args.run_id,
            "attempt_id": args.attempt_id, "execution_sha": args.execution_sha,
            "error_type": exc.__class__.__name__, "error": str(exc),
        }
        (args.output / "repair_failure.json").write_text(json.dumps(failure, sort_keys=True, indent=2))
        print(json.dumps(failure, sort_keys=True, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
