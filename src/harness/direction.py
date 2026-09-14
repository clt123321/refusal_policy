"""R0 direction extraction and selection-score primitives (pure functions).

Match V4_PREREGISTERED_CONSTANTS.json `r0_direction` exactly:
- direction: harmful_minus_harmless_difference_in_means
- selection_score: l2_norm(mean_diff) / sqrt(pooled_diag_variance + 1e-6)
- selection_rule: argmax with lowest layer index tie-break; selection on mechanism_dev only.

Engineering-validated only; no model, no data, no safety claim.
"""

from __future__ import annotations

import torch


def mean_difference_direction(harmful: torch.Tensor, harmless: torch.Tensor) -> torch.Tensor:
    """harmful/harmless: [n, d]. Returns normalized difference-in-means."""
    if harmful.ndim != 2 or harmless.ndim != 2:
        raise ValueError("expected 2-D [n, d] activations")
    diff = harmful.mean(dim=0) - harmless.mean(dim=0)
    norm = diff.norm()
    if norm == 0:
        raise ValueError("zero-norm difference-in-means; verify activation capture")
    return diff / norm


def selection_score(mean_diff: torch.Tensor, harmful: torch.Tensor, harmless: torch.Tensor) -> float:
    """l2_norm(mean_diff) / sqrt(pooled_diag_variance + 1e-6) summed over dims."""
    pooled_var = 0.5 * (harmful.var(dim=0, unbiased=True) + harmless.var(dim=0, unbiased=True))
    denom = torch.sqrt(pooled_var + 1e-6).sum()
    if denom == 0:
        raise ValueError("zero pooled variance denominator")
    return float(mean_diff.norm() / denom)


def select_layer(scores: dict[int, float]) -> int:
    """argmax score; lowest layer index ties-break."""
    best = max(scores, key=lambda k: (scores[k], -k))
    return best


def remove_projection(hidden: torch.Tensor, direction: torch.Tensor) -> torch.Tensor:
    unit = direction / direction.norm()
    projection = torch.einsum("...d,d->...", hidden, unit).unsqueeze(-1) * unit
    return hidden - projection


def add_direction(hidden: torch.Tensor, direction: torch.Tensor, alpha: float = 1.0) -> torch.Tensor:
    unit = direction / direction.norm()
    return hidden + alpha * unit


def orthogonalize_weights(W: torch.Tensor, direction: torch.Tensor) -> torch.Tensor:
    """W' = (I - rr^T) W. Verified invariant: r^T (W' x) = 0."""
    r = direction / direction.norm()
    return W - torch.outer(r, torch.einsum("i,ij->j", r, W))
