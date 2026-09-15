from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.execution.repair_runner import run_repair, verify_execution_checkout


def run_formal_repair(
    config_path: Path,
    parent_model_path: Path,
    output_dir: Path,
    *,
    arm: str,
    execution_sha: str,
    task_id: str,
    run_id: str,
    attempt_id: str,
    device: str = "cuda",
    repo: Path | None = None,
) -> dict[str, Any]:
    repo = (repo or Path(".")).resolve()
    verify_execution_checkout(repo, execution_sha)
    if arm not in {"C", "P"}:
        raise ValueError("FORMAL_REPAIR_ARM_INVALID")
    config = json.loads(config_path.read_text())
    if config.get("mode") != "FORMAL" or config.get("scientific_evidence") is not True:
        raise ValueError("FORMAL_REPAIR_CONFIG_REQUIRED")
    lineage = config.get("lineage", {})
    if lineage.get("arm") not in {"C", "P"}:
        raise ValueError("FORMAL_REPAIR_LINEAGE_ARM_REQUIRED")
    if lineage["arm"] != arm:
        raise ValueError("FORMAL_REPAIR_CONFIG_ARM_MISMATCH")
    return run_repair(
        config_path,
        parent_model_path,
        output_dir,
        device,
        execution_sha=execution_sha,
        task_id=task_id,
        run_id=run_id,
        attempt_id=attempt_id,
        repo=repo,
    )
