import torch

from src.harness.statistics import PairedArmSamples, paired_percentile_bootstrap


def test_paired_bootstrap_shape_consistency_and_runs():
    samples = PairedArmSamples(a=torch.ones(5, 20), b=torch.ones(5, 20))
    result = paired_percentile_bootstrap(samples, draws=100, seed=20260912)
    assert result["point_estimate"] == 1.0
    assert result["lower_90"] <= 1.0 <= result["upper_90"]
    assert result["draws_used"] == 100


def test_paired_bootstrap_detects_shift():
    samples = PairedArmSamples(a=torch.ones(5, 20) * 2.0, b=torch.ones(5, 20))
    result = paired_percentile_bootstrap(samples, draws=5000, seed=20260912)
    assert result["point_estimate"] > 1.5
    assert result["lower_90"] > 1.0


def test_paired_bootstrap_rejects_shape_mismatch():
    import pytest

    with pytest.raises(ValueError):
        PairedArmSamples(a=torch.ones(5, 20), b=torch.ones(4, 20))
    with pytest.raises(ValueError):
        PairedArmSamples(a=torch.ones(5, 20, 1), b=torch.ones(5, 20, 1))
