from src.data.proxy import build_proxy_assay, validate_assay
from src.interventions.proxy import add_direction, norm_matched_random, orthogonal_random, remove_projection
from src.stats.contrasts import bootstrap_mean, extract_contrasts
import torch


def test_proxy_assay_has_four_cells():
    rows = build_proxy_assay(2)
    validate_assay(rows)
    assert len(rows) == 8
    assert {(row["h"], row["p"]) for row in rows} == {(0, 0), (0, 1), (1, 0), (1, 1)}


def test_contrast_and_controls_are_deterministic():
    cells = {f"h{h}_p{p}": torch.ones(4) * (h + 2 * p + 1) for h in (0, 1) for p in (0, 1)}
    result = extract_contrasts(cells)
    assert torch.isclose(result["candidate_contrast_direction"].norm(), torch.tensor(1.0))
    assert torch.equal(norm_matched_random(result["p_contrast"], 7), norm_matched_random(result["p_contrast"], 7))
    assert torch.isclose(orthogonal_random(result["p_contrast"]).dot(result["p_contrast"]), torch.tensor(0.0), atol=1e-5)


def test_projection_operator_shapes():
    hidden = torch.randn(3, 4)
    direction = torch.randn(4)
    removed = remove_projection(hidden, direction)
    added = add_direction(hidden, direction, 0.5)
    assert removed.shape == hidden.shape
    assert added.shape == hidden.shape
    assert torch.allclose(removed @ direction, torch.zeros(3), atol=1e-4)


def test_bootstrap_has_interval():
    result = bootstrap_mean([0.0, 1.0, 2.0], seed=2, draws=100)
    assert result["ci_low"] <= result["mean"] <= result["ci_high"]
