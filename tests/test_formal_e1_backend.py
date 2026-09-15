from types import SimpleNamespace

import pytest

from src.execution.formal_e1_backend import ExecutorHookMissing, FormalE1Backend
from src.execution.formal_repair_entry import run_formal_repair


class FakeHooks:
    def run_a0(self, context): return {"valid": True, "artifact_id": "a0"}
    def run_repair(self, context, arm, parent): return {"valid": True, "arm": arm, "artifact_id": arm, "repair_stage": "r1"}
    def run_content_evaluator(self, context, artifact, split): return {"qualified": True, "split": split}
    def run_a1(self, context, arm, artifact): return {"valid": True, "first_qualified_workload": 4 if arm == "C" else (1 if arm == "P" else 2), "curve": [0, 1], "censoring": "none"}
    def run_plasticity(self, context, arm, artifact): return {"valid": True, "generic_plasticity_confound": False}


def context():
    return SimpleNamespace(state={"stages": {}})


def test_missing_hooks_are_explicit():
    with pytest.raises(ExecutorHookMissing, match="run_a0"):
        FormalE1Backend().pilot(context())


def test_full_fake_flow_and_pass_verdict():
    backend = FormalE1Backend(FakeHooks())
    ctx = context()
    pilot = backend.pilot(ctx); assert pilot["valid"]
    ctx.state["stages"]["pilot"] = {"result": pilot}
    construct = backend.construct(ctx); assert construct["valid"]
    ctx.state["stages"]["construct"] = {"result": construct}
    qualify = backend.qualify(ctx); assert qualify["valid"]
    ctx.state["stages"]["qualify"] = {"result": qualify}
    reattack = backend.reattack(ctx); assert reattack["valid"]
    ctx.state["stages"]["reattack"] = {"result": reattack}
    plasticity = backend.plasticity(ctx); assert plasticity["valid"]
    ctx.state["stages"]["plasticity"] = {"result": plasticity}
    verdict = backend.verdict(ctx)
    assert verdict["verdict"] == "V6_E1_PASS_REQUIRES_HUMAN_REVIEW"


def test_matching_failed_blocks_qualification():
    class Bad(FakeHooks):
        def run_content_evaluator(self, context, artifact, split): return {"qualified": False}
    backend = FormalE1Backend(Bad())
    ctx = context()
    pilot = backend.pilot(ctx); ctx.state["stages"]["pilot"] = {"result": pilot}
    ctx.state["stages"]["construct"] = {"result": backend.construct(ctx)}
    result = backend.qualify(ctx)
    assert result["valid"] is False
    assert result["classification"] == "MATCHING_FAILED"


def test_matching_failed_produces_invalid_without_a1_or_plasticity():
    class Bad(FakeHooks):
        def run_content_evaluator(self, context, artifact, split): return {"qualified": False, "split": split}
        def run_a1(self, context, arm, artifact): raise AssertionError("A1 must be skipped")
        def run_plasticity(self, context, arm, artifact): raise AssertionError("plasticity must be skipped")
    backend = FormalE1Backend(Bad()); ctx = context()
    for stage in ("pilot", "construct", "qualify"):
        result = getattr(backend, stage)(ctx); ctx.state["stages"][stage] = {"result": result}
    verdict = backend.verdict(ctx)
    assert verdict["valid"] is True
    assert verdict["verdict"] == "V6_E1_INVALID"
    assert verdict["reason"] == "MATCHING_FAILED"
    assert verdict["downstream_skipped"] == ["reattack", "plasticity"]


def test_censoring_is_preserved_and_verdict_inconclusive():
    class Censored(FakeHooks):
        def run_a1(self, context, arm, artifact): return {"valid": True, "first_qualified_workload": None, "censoring": "right"}
    backend = FormalE1Backend(Censored()); ctx = context()
    for stage in ("pilot", "construct", "qualify", "reattack", "plasticity"):
        result = getattr(backend, stage)(ctx); ctx.state["stages"][stage] = {"result": result}
    verdict = backend.verdict(ctx)
    assert verdict["verdict"] == "V6_E1_INCONCLUSIVE"
