#!/usr/bin/env python3
"""Static checks for the V6.E1 handoff plan; this is not an orchestrator."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import deque
from pathlib import Path


class PlanError(ValueError):
    pass


def validate_plan(path: Path) -> dict[str, int | bool]:
    plan = json.loads(path.read_text())
    if plan.get("experiment_id") != "V6.E1":
        raise PlanError("experiment_id must be V6.E1")
    tasks = plan.get("tasks", [])
    ids = [task.get("task_id") for task in tasks]
    if len(ids) != len(set(ids)):
        raise PlanError("task_id values must be unique")
    task_by_id = {task_id: task for task_id, task in zip(ids, tasks)}
    required = {
        "task_id", "mode", "arm", "run_id_template", "instances_ref",
        "depends_on", "conditions", "inputs", "operation", "entrypoint",
        "resource", "outputs", "completion", "current_status", "missing",
        "owner", "todo_clause",
    }
    for task in tasks:
        absent = required - set(task)
        if absent:
            raise PlanError(f"{task['task_id']} missing fields: {sorted(absent)}")
        unknown = set(task["depends_on"]) - set(ids)
        if unknown:
            raise PlanError(f"{task['task_id']} unknown dependencies: {sorted(unknown)}")

    indegree = {task_id: 0 for task_id in ids}
    children = {task_id: [] for task_id in ids}
    for task in tasks:
        for dependency in task["depends_on"]:
            indegree[task["task_id"]] += 1
            children[dependency].append(task["task_id"])
    queue = deque(task_id for task_id in ids if indegree[task_id] == 0)
    visited = 0
    while queue:
        task_id = queue.popleft()
        visited += 1
        for child in children[task_id]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if visited != len(ids):
        raise PlanError("dependency graph contains a cycle")

    repair_smoke = task_by_id["V6.E1.DEV.REPAIR_GPU_SMOKE"]
    forbidden_smoke_dependencies = {
        "V6.E1.DEV.EVALUATOR_AUTHORIZE", "V6.E1.DEV.A0_FREEZE",
        "V6.E1.DEV.DATA_FREEZE",
    }
    if forbidden_smoke_dependencies & set(repair_smoke["depends_on"]):
        raise PlanError("independent repair smoke has unrelated blockers")
    final_freeze = task_by_id["V6.E1.DEV.FREEZE"]
    candidate_to_preflight = {
        "V6.E1.DEV.REPAIR_FREEZE": "V6.E1.DEV.PREFLIGHT_REPAIR_A0",
        "V6.E1.DEV.A0_FREEZE": "V6.E1.DEV.PREFLIGHT_REPAIR_A0",
        "V6.E1.DEV.A1_FREEZE": "V6.E1.DEV.PREFLIGHT_A1",
    }
    for candidate, preflight in candidate_to_preflight.items():
        if candidate not in task_by_id[preflight]["depends_on"]:
            raise PlanError(f"{preflight} must depend on candidate lock {candidate}")
    for pilot in (
        "V6.E1.DEV.PREFLIGHT_REPAIR_A0", "V6.E1.DEV.PREFLIGHT_EVALUATOR",
        "V6.E1.DEV.PREFLIGHT_A1",
    ):
        if "V6.E1.DEV.FREEZE" in task_by_id[pilot]["depends_on"]:
            raise PlanError("pilot/preflight depends on final freeze")
        if pilot not in final_freeze["depends_on"]:
            raise PlanError("final freeze must depend on every preflight")
    expected_splits = {
        f"V6.E1.DEV.DATA.{name}" for name in (
            "D_A0_LOC", "D_REPAIR", "D_ENDPOINT_MATCH", "D_ENDPOINT_AUDIT",
            "D_A1_TRAIN", "D_ATTACK_EVAL", "D_FUNCTION", "D_PLASTICITY",
        )
    }
    if set(task_by_id["V6.E1.DEV.DATA_FREEZE"]["depends_on"]) != expected_splits:
        raise PlanError("aggregate data freeze must depend on all eight independent split tasks")
    summary = task_by_id["V6.E1.FORMAL.SUMMARY"]
    if summary.get("conditional_requires", {}).get("MATCHING_FAILED") != []:
        raise PlanError("MATCHING_FAILED must not wait for A1/plasticity")
    if set(summary.get("conditional_requires", {}).get("QUALIFIED", [])) != {
        "V6.E1.FORMAL.A1", "V6.E1.FORMAL.PLASTICITY",
    }:
        raise PlanError("QUALIFIED summary must wait for A1 and plasticity")
    if any("CONTINUOUS" in task_id or "QUEUE" in task_id for task_id in ids):
        raise PlanError("continuous/queue tasks are outside the direct E1 plan")
    dev_recipe_path = Path(plan["references"]["repair_dev_recipe"]["path"])
    dev_recipe = json.loads(dev_recipe_path.read_text())
    dev_data_path = Path(dev_recipe["data"]["path"])
    data_hash = hashlib.sha256(dev_data_path.read_bytes()).hexdigest()
    if data_hash != dev_recipe["data"]["file_sha256"]:
        raise PlanError("DEV repair fixture hash mismatch")
    ids = [json.loads(line)["id"] for line in dev_data_path.read_text().splitlines() if line.strip()]
    ids_raw = json.dumps(ids, sort_keys=True, separators=(",", ":")).encode()
    if hashlib.sha256(ids_raw).hexdigest() != dev_recipe["data"]["ids_sha256"]:
        raise PlanError("DEV repair fixture ID hash mismatch")
    return {"valid": True, "task_count": len(tasks), "edge_count": sum(len(task["depends_on"]) for task in tasks)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, nargs="?", default=Path("configs/execution/v6_e1_plan.json"))
    args = parser.parse_args(argv)
    print(json.dumps(validate_plan(args.path), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
