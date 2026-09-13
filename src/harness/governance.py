from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from src.harness.env import sha256_json


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class GovernanceRefusal(Exception):
    pass


class RunCard:
    REQUIRED = ("run_id", "repo_commit", "config_sha256", "seed", "stage", "gate", "status", "artifact_sha256", "executor")

    def __init__(self, **fields: Any):
        missing = [k for k in self.REQUIRED if k not in fields]
        if missing:
            raise GovernanceRefusal(f"RUN_CARD missing required fields: {missing}")
        self.fields = fields
        self.fields["created_utc"] = _now()

    def to_dict(self) -> dict[str, Any]:
        return self.fields


class ExperimentChangeCard:
    """Machine-readable change card (H7). Every field is required before a protocol change can execute."""

    REQUIRED = ("change_card_id", "baseline", "proposed_single_change", "reason", "prior_evidence", "predicted_effect", "falsifier", "controls", "compute_cost_estimate", "human_approval_required")

    def __init__(self, **fields: Any):
        missing = [k for k in self.REQUIRED if k not in fields]
        if missing:
            raise GovernanceRefusal(f"EXPERIMENT_CHANGE_CARD missing required fields: {missing}")
        if fields.get("human_approval_required") in (True, "true", "TRUE", "yes"):
            if not fields.get("approval_record"):
                raise GovernanceRefusal("EXPERIMENT_CHANGE_CARD requires human approval record when human_approval_required=true")
        self.fields = fields
        self.fields["hash"] = sha256_json({k: v for k, v in fields.items() if k != "hash"})

    def to_dict(self) -> dict[str, Any]:
        return self.fields


def refuse_unapproved_novel_defense(config: dict[str, Any]) -> None:
    if config.get("novel_defense") is True and not config.get("approved_change_card_id"):
        raise GovernanceRefusal("novel defense config requires approved EXPERIMENT_CHANGE_CARD")
