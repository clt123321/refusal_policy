from __future__ import annotations

from pathlib import Path

import pytest

from src.harness.adapters import BoundaryGuard, NoopAttackAdapter, NoopDefenseAdapter
from src.harness.artifact_store import ArtifactStore
from src.harness.cost_tracker import CostTracker, TrialRecord
from src.harness.env import EnvironmentLock, sha256_json
from src.harness.evaluators import SafetyEvaluator, SmartDeduplicator, UtilityEvaluator
from src.harness.governance import ExperimentChangeCard, GovernanceRefusal, RunCard, refuse_unapproved_novel_defense
from src.harness.manifest import ManifestValidationError, build_run_manifest, validate_manifest


def test_environment_lock_capture_has_required_fields():
    lock = EnvironmentLock.capture()
    for key in ("container_digest", "lock_sha256", "python", "pytorch", "cuda", "driver"):
        assert key in lock.as_manifest_field()


def test_cost_tracker_charges_failed_trials_and_censoring():
    tracker = CostTracker()
    tracker.add_trial(TrialRecord(trial_id=1, status="SUCCEEDED", estimated_flops=100.0))
    tracker.add_trial(TrialRecord(trial_id=2, status="FAILED", estimated_flops=50.0))
    tracker.add_trial(TrialRecord(trial_id=3, status="CENSORED", estimated_flops=25.0))
    assert tracker.cumulative_estimated_flops(3) == 175.0
    assert tracker.summary(3)["failed_trials"] == 1
    assert tracker.summary(3)["censored_status"] == "right"


def test_artifact_store_content_addressed_and_unique():
    store = ArtifactStore(Path("/tmp/harness_test_store_a"))
    d1 = store.store_bytes(b"hello", "greeting.txt")
    d2 = store.store_bytes(b"hello", "greeting2.txt")
    assert d1 == d2
    assert store.resolve("greeting.txt") is not None
    assert store.manifest_row("greeting.txt", d1, [])["sha256"] == d1


def test_manifest_schema_validation_accepts_valid_and_rejects_invalid():
    from src.harness.env import EnvironmentLock

    lock = EnvironmentLock.capture()
    manifest = build_run_manifest(
        run_id="harness.dry-run.0001",
        stage="R0",
        repo_commit="0" * 40,
        environment=lock.as_manifest_field(),
        model={"repo_id": "tiny", "revision": "0" * 40, "tokenizer_repo_id": "tiny", "tokenizer_revision": "0" * 40, "template_sha256": "0" * 64, "parent_artifact_ids": []},
        data=[{"name": "benign", "source_revision": "r1", "file_sha256": "0" * 64, "split": "utility", "ids_sha256": "0" * 64}],
        config={"benign": True},
        seed=17,
        hardware={"accelerator": "A800", "count": 1, "hostname_hash": "abc"},
        cost={"primary_estimated_flops": 1.0, "accelerator_seconds": 1.0, "wall_seconds": 1.0, "input_tokens": 1, "output_tokens": 1, "train_tokens": 0, "trials_attempted": 1, "failed_trials": 0, "peak_memory_bytes": 1},
        status="SUCCEEDED",
        artifacts=[{"role": "result", "uri": "x", "sha256": "0" * 64}],
    )
    assert manifest["schema_version"] == "4.0.0"
    bad = dict(manifest)
    bad["status"] = "NOT_A_STATUS"
    with pytest.raises(ManifestValidationError):
        validate_manifest(bad)


def test_utility_threshold_per_domain():
    evaluator = UtilityEvaluator()
    clean = {t: 0.8 for t in UtilityEvaluator.PREDEFINED_TASKS}
    attacked = {t: 0.79 for t in UtilityEvaluator.PREDEFINED_TASKS}
    result = evaluator.check_preservation(clean, attacked)
    assert all(result.values())
    attacked_bad = dict(attacked)
    attacked_bad["boolq"] = 0.5
    assert evaluator.check_preservation(clean, attacked_bad)["boolq"] is False


def test_boundary_guard_split_discipline():
    guard = BoundaryGuard()
    guard.assert_split_allowed("sealed_test")
    with pytest.raises(ValueError):
        guard.assert_split_allowed("anything_else")
    with pytest.raises(ValueError):
        guard.assert_test_blind("some-attack-dev-data", "sealed_test")
    guard.assert_test_blind("benign-data", "sealed_test")


def test_noop_adapter_round_trip():
    attack = NoopAttackAdapter()
    defense = NoopDefenseAdapter()
    assert attack.noop()["payload"] == "noop-round-trip"
    assert defense.noop()["payload"] == "noop-round-trip"
    assert "authorized executor" in attack.requires_authorized_executor()


def test_governance_refuses_incomplete_and_novel():
    with pytest.raises(GovernanceRefusal):
        RunCard(run_id="x")
    with pytest.raises(GovernanceRefusal):
        ExperimentChangeCard(change_card_id="x", baseline="b", proposed_single_change="c", reason="r", prior_evidence="e", predicted_effect="p", falsifier="f", controls="c", compute_cost_estimate="g", human_approval_required=True)
    with pytest.raises(GovernanceRefusal):
        refuse_unapproved_novel_defense({"novel_defense": True})
    refuse_unapproved_novel_defense({"novel_defense": False})


def test_safety_evaluator_seam_blocks_scoring():
    evaluator = SafetyEvaluator()
    assert "authorized executor" in evaluator.requires_authorized_executor()
    assert evaluator.refusal_diagnostics_fixture(["I'm sorry, I can't help.", "Mercury."])["refusal_rate"] == 0.5


def test_safety_content_aggregation_preserves_unknown():
    result = SafetyEvaluator().aggregate_content_labels(
        [{"classifier_label": "yes"}, {"classifier_label": "no"}, {"classifier_label": "UNKNOWN"}],
        model={"revision": "r"}, template_sha256="t", tokenizer_sha256="z",
    )
    assert result["valid"] == 2
    assert result["unknown"] == 1
    assert result["yes"] == 1
    assert result["no"] == 1


def test_endpoint_gate_requires_frozen_bands():
    evaluator = SafetyEvaluator()
    assert evaluator.evaluate_endpoint_gate({"safety": 0.9})["classification"] == "ENDPOINT_BANDS_NOT_FROZEN"
    result = evaluator.evaluate_endpoint_gate({"safety": 0.9}, {"safety": [0.8, 1.0]})
    assert result["qualified"] is True


def test_determinism_deduplicator():
    dedup = SmartDeduplicator("salt")
    assert not dedup.is_duplicate("a")
    assert dedup.is_duplicate("a")
    assert not dedup.is_duplicate("b")
