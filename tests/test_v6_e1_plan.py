import json
from pathlib import Path

from scripts.validate_v6_e1_plan import validate_plan


PLAN = Path("configs/execution/v6_e1_plan.json")


def test_v6_e1_plan_ids_dag_and_phase_semantics():
    result = validate_plan(PLAN)
    assert result["valid"] is True
    assert result["task_count"] >= 30


def test_blocked_evaluator_does_not_block_independent_repair_smoke():
    plan = json.loads(PLAN.read_text())
    tasks = {task["task_id"]: task for task in plan["tasks"]}
    dependencies = set(tasks["V6.E1.DEV.REPAIR_GPU_SMOKE"]["depends_on"])
    assert "V6.E1.DEV.EVALUATOR_AUTHORIZE" not in dependencies
    assert "V6.E1.DEV.DATA_FREEZE" not in dependencies
    assert "V6.E1.DEV.A0_FREEZE" not in dependencies
