from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class TrialRecord:
    trial_id: int
    status: str
    estimated_flops: float = 0.0
    accelerator_seconds: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0
    train_tokens: int = 0
    peak_memory_bytes: int = 0
    note: str = ""


class CostTracker:
    """V4 cost ledger: target-specific cumulative estimated FLOPs is the single primary axis;
    all others are mandatory secondary axes. Failed/OOM trials are always charged.
    Trial order follows logical trial ID, never parallel completion order."""

    def __init__(self, log_trial_order_by_id: bool = True):
        self.trials: dict[int, TrialRecord] = {}
        self._charge_logical_order = log_trial_order_by_id

    def add_trial(self, record: TrialRecord) -> None:
        self.trials[record.trial_id] = record

    def cumulative_estimated_flops(self, terminal_trial_id: int | None = None) -> float:
        ids = sorted(self.trials)
        if terminal_trial_id is not None:
            ids = [i for i in ids if i <= terminal_trial_id]
        return sum(self.trials[i].estimated_flops for i in ids)

    def summary(self, terminal_trial_id: int | None = None) -> dict[str, Any]:
        ids = sorted(self.trials)
        if terminal_trial_id is not None:
            ids = [i for i in ids if i <= terminal_trial_id]
        records = [self.trials[i] for i in ids]
        cumulative_flops = self.cumulative_estimated_flops(terminal_trial_id)
        return {
            "primary_estimated_flops": cumulative_flops,
            "target_specific_cumulative_estimated_flops": cumulative_flops,
            "accelerator_seconds": sum(r.accelerator_seconds for r in records),
            "input_tokens": sum(r.input_tokens for r in records),
            "output_tokens": sum(r.output_tokens for r in records),
            "train_tokens": sum(r.train_tokens for r in records),
            "trials_attempted": len(records),
            "failed_trials": sum(1 for r in records if r.status in ("FAILED", "OOM")),
            "peak_memory_bytes": max((r.peak_memory_bytes for r in records), default=0),
            "censored_status": self._censoring_status(terminal_trial_id),
        }

    def _censoring_status(self, terminal_trial_id: int | None) -> str:
        if terminal_trial_id is None:
            return "none"
        if terminal_trial_id in self.trials and self.trials[terminal_trial_id].status in ("CENSORED", "OOM"):
            return "right"
        return "none"

    def censoring_message(self, terminal_trial_id: int | None) -> str:
        if self._censoring_status(terminal_trial_id) != "none":
            return f"results right-censored at terminal trial {terminal_trial_id}; not 'breach cost'."
        return "no censoring"
