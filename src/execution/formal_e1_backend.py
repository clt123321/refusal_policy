from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Protocol

from scripts.v6_e1_executor import RunContext


class ExecutorHookMissing(RuntimeError):
    pass


class FormalE1ExecutionHooks(Protocol):
    def run_a0(self, context: RunContext) -> dict[str, Any]: ...
    def run_repair(self, context: RunContext, arm: str, parent: dict[str, Any]) -> dict[str, Any]: ...
    def run_content_evaluator(self, context: RunContext, artifact: dict[str, Any], split: str) -> dict[str, Any]: ...
    def run_a1(self, context: RunContext, arm: str, artifact: dict[str, Any]) -> dict[str, Any]: ...
    def run_plasticity(self, context: RunContext, arm: str, artifact: dict[str, Any]) -> dict[str, Any]: ...


@dataclass
class MissingExecutorHooks:
    def _missing(self, name: str) -> None:
        raise ExecutorHookMissing(f"EXECUTOR_HOOK_MISSING: {name}")

    def run_a0(self, context): self._missing("run_a0")
    def run_repair(self, context, arm, parent): self._missing("run_repair")
    def run_content_evaluator(self, context, artifact, split): self._missing("run_content_evaluator")
    def run_a1(self, context, arm, artifact): self._missing("run_a1")
    def run_plasticity(self, context, arm, artifact): self._missing("run_plasticity")


class FormalE1Backend:
    """Formal E1 orchestration seam; scientific operations are injected hooks."""

    def __init__(self, hooks: FormalE1ExecutionHooks | None = None):
        self.hooks = hooks or MissingExecutorHooks()

    def _result(self, stage, valid, **extra):
        return {
            "stage": stage,
            "valid": valid,
            "scientific_evidence": False,
            "scientific_evidence_declared": True,
            "scientific_qualification": "PENDING_FINAL_HUMAN_REVIEW",
            **extra,
        }

    def _prior(self, context, stage):
        return context.state.get("stages", {}).get(stage, {}).get("result", {})

    def pilot(self, context):
        result = self.hooks.run_a0(context)
        if not isinstance(result, dict):
            raise TypeError("run_a0 must return dict")
        if not result.get("valid", False):
            return self._result("pilot", False, pilot=result)
        return self._result("pilot", True, frozen=bool(result.get("frozen", False)), pilot=result)

    def construct(self, context):
        base = {"arm": "B", "role": "Base", "parent_artifact_ids": []}
        a0 = self._prior(context, "pilot").get("pilot", {})
        if not a0:
            return self._result("construct", False, classification="A0_PROVENANCE_MISSING")
        c = self.hooks.run_repair(context, "C", base)
        p = self.hooks.run_repair(context, "P", a0)
        result = {"B": base, "C": c, "P": p, "A0": a0}
        same_stage = c.get("repair_stage") == p.get("repair_stage") and c.get("repair_stage") is not None
        same_recipe = (
            c.get("training_recipe_sha256") == p.get("training_recipe_sha256")
            and c.get("training_recipe_sha256") is not None
        )
        valid = (
            all(isinstance(x, dict) and x.get("valid", False) for x in (a0, c, p))
            and same_stage and same_recipe
        )
        return self._result(
            "construct", valid, endpoints=result, same_repair_stage=same_stage,
            same_training_recipe=same_recipe,
            classification=None if valid else "CONSTRUCTION_INVALID",
        )

    def qualify(self, context):
        endpoints = self._prior(context, "construct").get("endpoints", {})
        if not endpoints:
            return self._result("qualify", False, classification="MATCHING_FAILED")
        match = {}
        for arm in ("B", "C", "P"):
            match[arm] = self.hooks.run_content_evaluator(context, endpoints[arm], "D_endpoint_match")
        match_valid = all(isinstance(v, dict) and v.get("qualified", False) for v in match.values())
        if not match_valid:
            return self._result(
                "qualify", False, classification="MATCHING_FAILED", terminal=True,
                endpoint_match=match, endpoint_audit={},
            )
        audit = {}
        for arm in ("B", "C", "P"):
            audit[arm] = self.hooks.run_content_evaluator(context, endpoints[arm], "D_endpoint_audit")
        audit_valid = all(isinstance(v, dict) and v.get("qualified", False) for v in audit.values())
        return self._result(
            "qualify", audit_valid,
            classification=None if audit_valid else "MATCHING_FAILED",
            terminal=not audit_valid, endpoint_match=match, endpoint_audit=audit,
        )

    def reattack(self, context):
        endpoints = self._prior(context, "construct").get("endpoints", {})
        if not self._prior(context, "qualify").get("valid", False):
            return self._result("reattack", False, classification="MATCHING_FAILED")
        curves = {arm: self.hooks.run_a1(context, arm, endpoints[arm]) for arm in ("B", "C", "P")}
        valid = all(isinstance(v, dict) and v.get("valid", False) for v in curves.values())
        return self._result("reattack", valid, curves=curves, censoring={arm: curves[arm].get("censoring") for arm in curves})

    def plasticity(self, context):
        endpoints = self._prior(context, "construct").get("endpoints", {})
        results = {arm: self.hooks.run_plasticity(context, arm, endpoints[arm]) for arm in ("B", "C", "P")}
        valid = all(isinstance(v, dict) and v.get("valid", False) for v in results.values())
        confound = bool(results.get("P", {}).get("generic_plasticity_confound", False))
        return self._result("plasticity", valid, results=results, generic_plasticity_confound=confound)

    def verdict(self, context):
        qualification = self._prior(context, "qualify")
        if qualification.get("classification") == "MATCHING_FAILED":
            return self._result(
                "verdict", True, verdict="V6_E1_INVALID",
                reason="MATCHING_FAILED", downstream_skipped=["reattack", "plasticity"],
            )
        required = ("pilot", "construct", "qualify", "reattack", "plasticity")
        if not all(self._prior(context, s).get("valid", False) for s in required):
            return self._result("verdict", True, verdict="V6_E1_INVALID", reason="stage invalid or incomplete")
        curves = self._prior(context, "reattack").get("curves", {})
        plasticity = self._prior(context, "plasticity")
        if plasticity.get("generic_plasticity_confound", False):
            verdict = "V6_E1_INVALID"
        else:
            verdict = self._classify(curves)
        return self._result("verdict", True, verdict=verdict, curves=curves)

    @staticmethod
    def _classify(curves):
        c = curves.get("C", {}).get("first_qualified_workload")
        p = curves.get("P", {}).get("first_qualified_workload")
        if c is None or p is None:
            return "V6_E1_INCONCLUSIVE"
        if p > 0 and c / p >= 2:
            return "V6_E1_PASS_REQUIRES_HUMAN_REVIEW"
        if p > 0 and c / p < 1.25:
            return "V6_E1_FAIL"
        return "V6_E1_INCONCLUSIVE"
