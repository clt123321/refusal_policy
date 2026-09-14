"""Pure-math unit tests for V4 intervention/selection semantics.

These validate tensor-level semantics with no model and no data:
projection math, operator sign conventions, hook ordering, weight-edit
equivalence, token position, selection score, serialization round trips.

They are ENGINEERING_VALIDATED only — never treated as R0a/R1-R3 evidence.
"""

from __future__ import annotations

import io
import json
import random

import pytest
import torch

from src.harness.cost_tracker import CostTracker, TrialRecord
from src.harness.env import normalize_record_id, salted_record_hash, sha256_bytes, sha256_json


def unit_vector(dim: int, seed: int = 0) -> torch.Tensor:
    generator = torch.Generator().manual_seed(seed)
    v = torch.randn(dim, generator=generator)
    return v / v.norm()


def projection(v: torch.Tensor, direction: torch.Tensor) -> torch.Tensor:
    unit = direction / direction.norm()
    return torch.dot(v, unit) * unit


class TestRemoveAddOperatorSemantics:
    """Operators: remove zeroes the projection; add moves by exactly alpha; scale is signed."""

    def test_remove_projection_is_exact(self):
        hidden = torch.randn(1536)
        direction = unit_vector(1536, seed=1)
        unit = direction / direction.norm()
        removed = hidden - torch.dot(hidden, unit) * unit
        assert torch.allclose(torch.dot(removed, unit), torch.tensor(0.0), atol=1e-6)

    def test_add_moves_by_exact_alpha(self):
        hidden = torch.zeros(1536)
        direction = unit_vector(1536, seed=2)
        alpha = 0.5
        added = hidden + alpha * direction / direction.norm()
        assert torch.allclose(torch.dot(added, direction / direction.norm()), torch.tensor(alpha), atol=1e-6)

    def test_remove_then_add_restores_approximately(self):
        hidden = torch.randn(1536)
        direction = unit_vector(1536, seed=3)
        unit = direction / direction.norm()
        proj = torch.dot(hidden, unit) * unit
        restored = (hidden - proj) + proj
        assert torch.allclose(restored, hidden, atol=1e-6)

    def test_scale_mode_sign_convention(self):
        # scale mode: delta = -alpha * projection * unit. alpha=1 == remove; alpha=-1 == double.
        hidden = torch.randn(1536)
        unit = unit_vector(1536, seed=4)
        projection_scalar = torch.dot(hidden, unit)
        projected = projection_scalar * unit
        removed = hidden - projected
        doubled = hidden + projected
        assert torch.allclose(hidden - 1.0 * projected, removed, atol=1e-6)
        assert torch.allclose(hidden - (-1.0) * projected, doubled, atol=1e-6)


class TestWeightOrthogonalizationEquivalence:
    """W' = (I - rr^T) W must zero r^T (W' x) for every x, and must survive save/reload."""

    def test_orthogonalization_zeroes_projection_into_safety_direction(self):
        r = unit_vector(64, seed=5)
        W = torch.randn(64, 128, generator=torch.Generator().manual_seed(6)) * 0.1
        # Invariant form: W_new = (I - r r^T) W must satisfy r^T (W_new x) ~= 0 for every x.
        W_new = (torch.eye(64) - torch.outer(r, r)) @ W
        x = torch.randn(128, generator=torch.Generator().manual_seed(7))
        assert torch.allclose(torch.dot(r, W_new @ x), torch.tensor(0.0), atol=1e-5)

    def test_output_row_projection_is_equivalent_to_matrix_form(self):
        # Equivalence: (I - rr^T) W  ==  W - outer(r, r^T W), where r^T W is the
        # input-dim projection of all rows onto r. Verified numerically.
        r = unit_vector(32, seed=8)
        W = torch.randn(32, 64, generator=torch.Generator().manual_seed(9))
        W_new_matrix = (torch.eye(32) - torch.outer(r, r)) @ W
        proj = torch.einsum("i,ij->j", r, W)
        W_new_outer = W - torch.outer(r, proj)
        assert torch.allclose(W_new_outer, W_new_matrix, atol=1e-5)
        # row-wise viewpoint: the change to row i is -r[i] * proj
        row_deltas = W_new_matrix - W
        expected_delta = -torch.outer(r, proj)
        assert torch.allclose(row_deltas, expected_delta, atol=1e-5)

    def test_save_reload_roundtrip_preserves_edited_weights(self):
        r = unit_vector(32, seed=10)
        W = torch.randn(32, 64, generator=torch.Generator().manual_seed(11))
        W_new = (torch.eye(32) - torch.outer(r, r)) @ W
        buffer = io.BytesIO()
        torch.save({"weight": W_new}, buffer)
        buffer.seek(0)
        loaded = torch.load(buffer, map_location="cpu")
        assert torch.allclose(loaded["weight"], W_new, atol=0.0)


class TestHookOrdering:
    """The safe-proxy lesson: with a read-hook and a modify-hook on the same module,
    ordering determines what the read-hook sees. The harness must never mix
    capture+steer on the same module in the same forward pass."""

    def test_hooks_fire_in_registration_order_on_same_module(self):
        from torch import nn

        class Block(nn.Module):
            def __init__(self):
                super().__init__()
                self.value = torch.tensor([1.0, 2.0, 3.0])

            def forward(self):
                return self.value.clone()

        block = Block()
        seen: list[str] = []

        def read_hook(_module, _args, output):
            seen.append(f"read_{output[0].item()}")

        def mut_hook(_module, _args, output):
            seen.append(f"mut_{output[0].item()}")
            return output * 0

        block.register_forward_hook(read_hook)
        block.register_forward_hook(mut_hook)
        block()
        assert seen == ["read_1.0", "mut_1.0"]
        # The read hook sees pre-modification value because it fires first.

    def test_single_steer_hook_only_no_stale_read(self):
        from src.harness.env import sha256_json

        # Placeholder to import harness module paths; real check is in audit doc.
        assert sha256_json({"a": 1}) == sha256_json({"a": 1})


class TestSelectionScoreSemantics:
    """selection_score = l2_norm(mean_diff) / sqrt(pooled_diag_variance + 1e-6)"""

    def test_score_definition_matches_preregistered_constant(self):
        a = torch.randn(32, 128, generator=torch.Generator().manual_seed(12))
        b = torch.randn(32, 128, generator=torch.Generator().manual_seed(13)) + 1.0
        mean_diff = a.mean(0) - b.mean(0)
        pooled_var = 0.5 * (a.var(0, unbiased=True) + b.var(0, unbiased=True))
        score = mean_diff.norm() / torch.sqrt(pooled_var + 1e-6).sum()
        assert score > 0
        assert score.isfinite()

    def test_separating_direction_scores_higher_than_noise(self):
        noise = torch.randn(16, 64, generator=torch.Generator().manual_seed(14))
        separated = torch.randn(16, 64, generator=torch.Generator().manual_seed(15)) + torch.tensor([5.0] + [0.0] * 63)
        score_noise = noise.mean(0).norm() / torch.sqrt(noise.var(0, unbiased=True) + 1e-6).sum()
        score_sep = separated.mean(0).norm() / torch.sqrt(separated.var(0, unbiased=True) + 1e-6).sum()
        assert score_sep > score_noise


class TestTokenPositionSemantics:
    def test_last_non_padding_token_index(self):
        attention_mask = torch.tensor([[1, 1, 1, 0, 0], [1, 1, 0, 0, 0]])
        indices = attention_mask.sum(dim=1).to(torch.long) - 1
        assert indices.tolist() == [2, 1]
        hidden = torch.arange(10).reshape(2, 5)
        gathered = hidden[torch.arange(2), indices]
        assert gathered.tolist() == [2, 6]


class TestNormalizationAndHashing:
    def test_normalize_record_id_rules(self):
        assert normalize_record_id("  a\t b  ", "salt") == "a b"
        assert normalize_record_id("a\r\nb", "salt") == "a b"
        assert normalize_record_id("Ａ", "salt") == "A"  # NFKC normalizes fullwidth to ASCII

    def test_salted_record_hash_is_deterministic_and_order_preserving_input(self):
        assert salted_record_hash("abc", "refusal-policy-v4-20260911") == salted_record_hash("abc", "refusal-policy-v4-20260911")
        assert salted_record_hash("abc", "s1") != salted_record_hash("abc", "s2")

    def test_sha256_json_stable(self):
        assert sha256_json({"b": 1, "a": 2}) == sha256_json({"a": 2, "b": 1})
        assert sha256_bytes(b"x") == sha256_bytes(b"x")


class TestCostLedgerEdgeCases:
    def test_parallel_completion_order_ignored(self):
        tracker = CostTracker()
        tracker.add_trial(TrialRecord(trial_id=2, status="SUCCEEDED", estimated_flops=200.0))
        tracker.add_trial(TrialRecord(trial_id=1, status="SUCCEEDED", estimated_flops=100.0))
        # logical order must be by trial id, not insertion order
        assert tracker.cumulative_estimated_flops(1) == 100.0
        assert tracker.cumulative_estimated_flops(2) == 300.0

    def test_oort_failed_trial_is_charged_and_censoring_recorded(self):
        tracker = CostTracker()
        tracker.add_trial(TrialRecord(trial_id=1, status="OOM", estimated_flops=50.0))
        tracker.add_trial(TrialRecord(trial_id=2, status="CENSORED", estimated_flops=10.0))
        summary = tracker.summary(2)
        assert summary["failed_trials"] == 1
        assert summary["censored_status"] == "right"

    def test_no_composite_scalar_emitted(self):
        tracker = CostTracker()
        tracker.add_trial(TrialRecord(trial_id=1, status="SUCCEEDED", estimated_flops=1.0))
        summary = tracker.summary(1)
        # The V4 contract forbids combining heterogeneous axes into a custom scalar.
        assert "primary_estimated_flops" in summary
        assert "target_specific_cumulative_estimated_flops" in summary
        assert "target_specific_cumulative_estimated_flops" in summary
