import torch

from src.harness.direction import add_direction, mean_difference_direction, orthogonalize_weights, remove_projection, select_layer, selection_score


def test_mean_difference_direction_is_normalized():
    harmful = torch.randn(256, 32) + torch.tensor([3.0] + [0.0] * 31)
    harmless = torch.randn(256, 32)
    direction = mean_difference_direction(harmful, harmless)
    assert torch.allclose(direction.norm(), torch.tensor(1.0), atol=1e-5)
    # 1 of 32 dims offset by 3.0 -> expected share ~3/sqrt(3^2+31) ~ 0.47; require > 0.3
    assert direction[0] > 0.3


def test_selection_score_prefers_separated():
    harmful = torch.randn(64, 128) + torch.tensor([2.0] + [0.0] * 127)
    harmless = torch.randn(64, 128)
    diff = harmful.mean(0) - harmless.mean(0)
    score = selection_score(diff, harmful, harmless)
    noise_h = torch.randn(64, 128)
    noise_l = torch.randn(64, 128)
    noise_diff = noise_h.mean(0) - noise_l.mean(0)
    noise_score = selection_score(noise_diff, noise_h, noise_l)
    assert score > noise_score


def test_select_layer_argmax_with_tie_break():
    scores = {1: 1.5, 2: 1.5, 3: 3.0}
    assert select_layer(scores) == 3
    assert select_layer({5: 2.0, 2: 2.0}) == 2  # lowest layer index tie-break


def test_remove_projection_zeroes_along_direction():
    hidden = torch.randn(4, 128)
    direction = torch.randn(128)
    unit = direction / direction.norm()
    removed = remove_projection(hidden, direction)
    assert torch.allclose(removed @ unit, torch.zeros(4), atol=1e-6)


def test_add_direction_moves_by_alpha():
    hidden = torch.zeros(128)
    direction = torch.randn(128)
    unit = direction / direction.norm()
    added = add_direction(hidden, direction, alpha=2.0)
    assert torch.allclose(torch.dot(added, unit), torch.tensor(2.0), atol=1e-6)


def test_orthogonalize_weights_invariant():
    r = torch.randn(32)
    W = torch.randn(32, 64) * 0.1
    W_new = orthogonalize_weights(W, r)
    x = torch.randn(64)
    assert torch.allclose(torch.dot(r / r.norm(), W_new @ x), torch.tensor(0.0), atol=1e-5)


def test_mean_difference_zero_norm_raises():
    import pytest

    harmful = torch.zeros(8, 4)
    harmless = torch.zeros(8, 4)
    with pytest.raises(ValueError):
        mean_difference_direction(harmful, harmless)
