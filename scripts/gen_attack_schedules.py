"""Deterministic logical-trial scheduler for the frozen A1/R2 cells.

Generates the frozen 35-candidate A1 grid order (rank ascending, then strength
ascending) and the A3 24-candidate LoRA order with deterministic trial IDs,
matching V4_PREREGISTERED_CONSTANTS.json. No execution, no attacks.

Purpose: prove the deterministic anytime schedule and tier assignment so the
R2 execution, when authorized, runs with a pre-agreed logical order.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

CONSTANTS_PATH = Path("research/protocols/V4_PREREGISTERED_CONSTANTS.json")


def load_constants() -> dict:
    return json.loads(CONSTANTS_PATH.read_text())


def a1_grid_order(constants: dict) -> list[dict]:
    a1 = constants["a1_directional_edit"]
    ranks = a1["ranks"]
    strengths = a1["strengths"]
    assert a1["candidate_order"] == "rank ascending, then strength ascending"
    candidates = []
    for rank in ranks:
        for strength in strengths:
            candidates.append({"rank": rank, "strength": strength})
    return candidates


def tier_assignment(candidates: list[dict], terminal_ids: list[int]) -> dict[int, list[int]]:
    """Each tier covers candidates up to its terminal trial id (inclusive)."""
    tiers: dict[int, list[int]] = {}
    prev = 0
    for tier, terminal in enumerate(terminal_ids, start=1):
        tiers[tier] = list(range(prev + 1, terminal + 1))
        prev = terminal
    return tiers


def a3_grid_order(constants: dict) -> list[dict]:
    a3 = constants["a3_lora"]
    candidates = []
    for rank in a3["ranks"]:
        for lr in a3["learning_rates"]:
            for steps in a3["steps"]:
                candidates.append({"rank": rank, "learning_rate": lr, "steps": steps})
    return candidates


def full_ft_order(constants: dict) -> list[dict]:
    fft = constants["full_ft_sentinel"]
    return [{"learning_rate": lr, "data_order": order} for lr in fft["learning_rates"] for order in fft["data_orders"]]


def write_r2_schedule() -> None:
    constants = load_constants()
    a1 = a1_grid_order(constants)
    tiers = tier_assignment(a1, constants["a1_directional_edit"]["budget_tier_terminal_trial_ids"])
    schedule = {
        "cell": "R2-A1-base-only",
        "trial_count": len(a1),
        "order_rule": constants["a1_directional_edit"]["candidate_order"],
        "tiers": tiers,
        "trials": [{"trial_id": i, **c} for i, c in enumerate(a1, start=1)],
    }
    out = Path("configs/execution/r2_a1_schedule.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(schedule, indent=2))
    print(f"R2 A1 schedule: {len(a1)} trials, {len(tiers)} tiers -> {out}")


def write_a3_lora_schedule() -> None:
    constants = load_constants()
    candidates = a3_grid_order(constants)
    schedule = {
        "cell": "A3-LoRA-grid",
        "trial_count": len(candidates),
        "order_rule": constants["a3_lora"]["candidate_order"],
        "trials": [{"trial_id": i, **c} for i, c in enumerate(candidates, start=1)],
        "full_ft_sentinel": [{"trial_id": i, **c} for i, c in enumerate(full_ft_order(constants), start=1)],
    }
    out = Path("configs/execution/a3_lora_schedule.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(schedule, indent=2))
    print(f"A3 LoRA schedule: {len(candidates)} trials -> {out}")


if __name__ == "__main__":
    write_r2_schedule()
    write_a3_lora_schedule()
