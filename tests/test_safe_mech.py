import torch
import torch.nn as nn

from src.data.safe_mech import build_safe_mech_assay, validate_safe_mech_assay
from src.eval.policy_classifier import classify_policy, is_compliant
from src.interventions.generation import steer_layer
from src.stats.contrasts import bootstrap_paired_diff, shuffled_label_cells


def test_safe_mech_assay_structure():
    rows = build_safe_mech_assay(4)
    validate_safe_mech_assay(rows)
    instructed = [r for r in rows if r["policy"] in ("answer", "abstain")]
    natural = [r for r in rows if r["policy"] == "natural"]
    assert len(instructed) == 2 * 3 * 2 * 4
    assert len(natural) == 2 * 3 * 4


def test_policy_classifier_basic():
    assert classify_policy("I am not able to help with this right now.", "astronomy") == "abstain"
    assert classify_policy("A black hole is an astronomical object with strong gravity.", "astronomy") == "answer"
    assert classify_policy("", "astronomy") == "invalid"
    assert is_compliant("answer") and not is_compliant("abstain")


class _EchoLayer(nn.Module):
    def forward(self, hidden):
        return (hidden,)


def test_steer_layer_remove_zeroes_projection():
    layer = _EchoLayer()
    direction = torch.tensor([1.0, 0.0, 0.0])
    hidden = torch.tensor([[[3.0, 2.0, 1.0]]])
    with steer_layer(_wrap(layer), 0, "remove", direction):
        out = layer(hidden)[0]
    assert torch.allclose(out, torch.tensor([[[0.0, 2.0, 1.0]]]))


def test_steer_layer_add_shifts_along_direction():
    layer = _EchoLayer()
    direction = torch.tensor([0.0, 1.0, 0.0])
    hidden = torch.zeros(1, 1, 3)
    with steer_layer(_wrap(layer), 0, "add", direction, alpha=2.0):
        out = layer(hidden)[0]
    assert torch.allclose(out, torch.tensor([[[0.0, 2.0, 0.0]]]))


class _ModelStub:
    def __init__(self, layer):
        self.model = _ModelInner(layer)


class _ModelInner:
    def __init__(self, layer):
        self.layers = [layer]


def _wrap(layer):
    return _ModelStub(layer)


def test_shuffled_label_cells_preserves_count():
    cells = {f"h{h}_p{p}": [torch.randn(4) for _ in range(6)] for h in (0, 1) for p in (0, 1)}
    shuffled = shuffled_label_cells(cells, seed=3)
    assert sum(len(v) for v in shuffled.values()) == sum(len(v) for v in cells.values())


def test_bootstrap_paired_diff_zero_when_identical():
    result = bootstrap_paired_diff([1.0, 0.0, 1.0, 0.0], [1.0, 0.0, 1.0, 0.0])
    assert result["mean_diff"] == 0.0
    assert result["ci_low"] <= 0.0 <= result["ci_high"]
