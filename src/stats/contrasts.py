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
    return {
        "candidate_contrast_direction": normalized(p),
        "h_contrast": normalized(h),
        "p_contrast": normalized(p),
        "h_x_p_interaction": interaction,
        "raw_h_contrast": h,
        "raw_p_contrast": p,
    }


def cell_means_from_examples(cells: dict[str, list[torch.Tensor]]) -> dict[str, torch.Tensor]:
    return {key: torch.stack(values).mean(dim=0) for key, values in cells.items()}


def bootstrap_direction_stability(cells: dict[str, list[torch.Tensor]], seed: int = 17, draws: int = 200, direction_key: str = "p_contrast") -> dict[str, float]:
    generator = torch.Generator().manual_seed(seed)
    base_direction = extract_contrasts(cell_means_from_examples(cells))[direction_key]
    stacked = {key: torch.stack(values) for key, values in cells.items()}
    cosines = []
    for _ in range(draws):
        resampled_means = {}
        for key, values in stacked.items():
            n = values.shape[0]
            idx = torch.randint(n, (n,), generator=generator)
            resampled_means[key] = values[idx].mean(dim=0)
        direction = extract_contrasts(resampled_means)[direction_key]
        cosines.append(cosine(direction, base_direction))
    cosines_t = torch.tensor(cosines)
    return {
        "mean_cosine": float(cosines_t.mean()),
        "ci_low": float(torch.quantile(cosines_t, 0.025)),
        "ci_high": float(torch.quantile(cosines_t, 0.975)),
        "frac_abs_cosine_ge_0.8": float((cosines_t.abs() >= 0.8).float().mean()),
    }


def leave_one_family_out_stability(rows: list[dict], vectors_by_example: dict[str, torch.Tensor], direction_key: str = "p_contrast") -> dict[str, float]:
    families = sorted({row["family"] for row in rows if row["family"] is not None})
    full_cells: dict[str, list[torch.Tensor]] = {}
    for row in rows:
        if row["p"] is None:
            continue
        full_cells.setdefault(f"h{row['h']}_p{row['p']}", []).append(vectors_by_example[row["example_id"]])
    base_direction = extract_contrasts(cell_means_from_examples(full_cells))[direction_key]
    cosines = []
    for held_out in families:
        cells: dict[str, list[torch.Tensor]] = {}
        for row in rows:
            if row["p"] is None or row["family"] == held_out:
                continue
            cells.setdefault(f"h{row['h']}_p{row['p']}", []).append(vectors_by_example[row["example_id"]])
        direction = extract_contrasts(cell_means_from_examples(cells))[direction_key]
        cosines.append(cosine(direction, base_direction))
    cosines_t = torch.tensor(cosines)
    return {"mean_cosine": float(cosines_t.mean()), "min_cosine": float(cosines_t.min()), "n_families": len(families)}


def bootstrap_paired_diff(main: list[float], control: list[float], seed: int = 17, draws: int = 2000) -> dict[str, float]:
    if len(main) != len(control):
        raise ValueError("main and control must be paired and equal length")
    generator = torch.Generator().manual_seed(seed)
    main_t = torch.tensor(main, dtype=torch.float64)
    control_t = torch.tensor(control, dtype=torch.float64)
    n = len(main)
    indices = torch.randint(n, (draws, n), generator=generator)
    diffs = main_t[indices].mean(dim=1) - control_t[indices].mean(dim=1)
    return {
        "mean_diff": float(main_t.mean() - control_t.mean()),
        "ci_low": float(torch.quantile(diffs, 0.025)),
        "ci_high": float(torch.quantile(diffs, 0.975)),
    }


def shuffled_label_cells(cells: dict[str, list[torch.Tensor]], seed: int = 17) -> dict[str, list[torch.Tensor]]:
    generator = torch.Generator().manual_seed(seed)
    all_vectors: list[torch.Tensor] = []
    all_h: list[int] = []
    for key, vectors in cells.items():
        h_val = int(key.split("_")[0][1:])
        for vector in vectors:
            all_vectors.append(vector)
            all_h.append(h_val)
    n = len(all_vectors)
    perm = torch.randperm(n, generator=generator).tolist()
    half = n // 2
    shuffled_p = [0] * n
    for rank, idx in enumerate(perm):
        shuffled_p[idx] = 0 if rank < half else 1
    shuffled: dict[str, list[torch.Tensor]] = {}
    for vector, h_val, p_val in zip(all_vectors, all_h, shuffled_p):
        shuffled.setdefault(f"h{h_val}_p{p_val}", []).append(vector)
    return shuffled


def cosine(a: torch.Tensor, b: torch.Tensor) -> float:
    return float(torch.nn.functional.cosine_similarity(a.flatten(), b.flatten(), dim=0))


def policy_subspace_directions(cells: dict[str, list[torch.Tensor]], k: int) -> torch.Tensor:
    h_groups: dict[int, list[torch.Tensor]] = {}
    for key, vectors in cells.items():
        h_val = int(key.split("_")[0][1:])
        h_groups.setdefault(h_val, []).extend(vectors)
    residuals = []
    for h_val, vectors in h_groups.items():
        stacked = torch.stack(vectors)
        mean = stacked.mean(dim=0)
        residuals.append(stacked - mean)
    matrix = torch.cat(residuals, dim=0)
    _, _, vt = torch.linalg.svd(matrix, full_matrices=False)
    return vt[:k]


def bootstrap_mean(values: list[float], seed: int = 17, draws: int = 1000) -> dict[str, float]:
    if not values:
        raise ValueError("bootstrap requires values")
    generator = torch.Generator().manual_seed(seed)
    sample = torch.tensor(values, dtype=torch.float64)
    indices = torch.randint(len(values), (draws, len(values)), generator=generator)
    means = sample[indices].mean(dim=1)
    return {"mean": float(sample.mean()), "ci_low": float(torch.quantile(means, 0.025)), "ci_high": float(torch.quantile(means, 0.975))}
