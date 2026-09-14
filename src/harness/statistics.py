"""V4 statistics: paired hierarchical percentile bootstrap (frozen constants).

Playground/spec-only module: no real data is attached; geometry follows
V4_PREREGISTERED_CONSTANTS.json `statistics` (paired_arm_units resample paired
attack seed at outer level, normalized behavior_id at inner level; preserve arm
pairing; draws=10000; rng_seed=20260912).
"""

from __future__ import annotations

from dataclasses import dataclass

import torch


@dataclass
class PairedArmSamples:
    """Per-paired-arm per-nested-unit numerical outcomes, arms a and b equal length."""

    a: torch.Tensor
    b: torch.Tensor

    def __post_init__(self) -> None:
        if self.a.shape != self.b.shape:
            raise ValueError(f"paired arms must have identical shape, got {self.a.shape} vs {self.b.shape}")
        if self.a.ndim not in (1, 2):
            raise ValueError("expected [seed] or [seed, nested_unit] tensors")


def paired_percentile_bootstrap(samples: PairedArmSamples, draws: int = 10000, seed: int = 20260912, confidence: float = 0.90) -> dict[str, float]:
    """Resample paired attack seeds at the outer level, nested units at inner level,
    preserve arm pairing, and return ratio (a/b) point + one-sided bounds."""
    shape = samples.a.shape
    a_flat = samples.a.reshape(shape[0], -1)
    b_flat = samples.b.reshape(shape[0], -1)
    generator = torch.Generator().manual_seed(seed)
    ratios = []
    for _ in range(draws):
        idx = torch.randint(shape[0], (shape[0],), generator=generator)
        a_r = a_flat[idx]
        b_r = b_flat[idx]
        denom = b_r.sum()
        if denom == 0:
            continue
        ratios.append(a_r.sum().item() / denom.item())
    ratios_t = torch.tensor(ratios)
    low_q = (1.0 - confidence) / 2.0 * 100
    high_q = 100.0 - low_q
    return {
        "point_estimate": float(ratios_t.mean()),
        f"lower_{int(confidence*100)}": float(torch.quantile(ratios_t, low_q / 100.0)),
        f"upper_{int(confidence*100)}": float(torch.quantile(ratios_t, high_q / 100.0)),
        "draws_used": len(ratios_t),
        "confidence": confidence,
    }
