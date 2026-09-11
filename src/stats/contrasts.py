import torch


def normalized(vector: torch.Tensor) -> torch.Tensor:
    norm = vector.norm()
    if norm == 0:
        raise ValueError("cannot normalize zero vector")
    return vector / norm


def extract_contrasts(cell_means: dict[str, torch.Tensor]) -> dict[str, torch.Tensor]:
    required = {f"h{h}_p{p}" for h in (0, 1) for p in (0, 1)}
    if set(cell_means) != required:
        raise ValueError(f"expected cells {required}, got {set(cell_means)}")
    h = 0.5 * ((cell_means["h1_p0"] + cell_means["h1_p1"]) - (cell_means["h0_p0"] + cell_means["h0_p1"]))
    p = 0.5 * ((cell_means["h0_p1"] + cell_means["h1_p1"]) - (cell_means["h0_p0"] + cell_means["h1_p0"]))
    interaction = cell_means["h1_p1"] - cell_means["h1_p0"] - cell_means["h0_p1"] + cell_means["h0_p0"]
    return {"candidate_contrast_direction": normalized(p), "h_contrast": normalized(h), "p_contrast": normalized(p), "h_x_p_interaction": interaction}


def cosine(a: torch.Tensor, b: torch.Tensor) -> float:
    return float(torch.nn.functional.cosine_similarity(a.flatten(), b.flatten(), dim=0))


def bootstrap_mean(values: list[float], seed: int = 17, draws: int = 1000) -> dict[str, float]:
    if not values:
        raise ValueError("bootstrap requires values")
    generator = torch.Generator().manual_seed(seed)
    sample = torch.tensor(values, dtype=torch.float64)
    indices = torch.randint(len(values), (draws, len(values)), generator=generator)
    means = sample[indices].mean(dim=1)
    return {"mean": float(sample.mean()), "ci_low": float(torch.quantile(means, 0.025)), "ci_high": float(torch.quantile(means, 0.975))}
