import argparse
import json
from pathlib import Path

import torch

from src.data.safe_mech import build_safe_mech_assay, validate_safe_mech_assay
from src.hooks.multi_capture import collect_all_layer_means
from src.models.runtime import load_model
from src.stats.contrasts import (
    bootstrap_direction_stability,
    cell_means_from_examples,
    cosine,
    extract_contrasts,
    leave_one_family_out_stability,
)


def project_separation(direction: torch.Tensor, vectors_a: list[torch.Tensor], vectors_b: list[torch.Tensor]) -> float:
    unit = direction / direction.norm()
    proj_a = torch.stack([torch.dot(v, unit) for v in vectors_a])
    proj_b = torch.stack([torch.dot(v, unit) for v in vectors_b])
    pooled_std = torch.sqrt(0.5 * (proj_a.var(unbiased=True) + proj_b.var(unbiased=True))) + 1e-8
    return float((proj_a.mean() - proj_b.mean()) / pooled_std)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="Qwen/Qwen2.5-1.5B-Instruct")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--dtype", default="float16")
    parser.add_argument("--n-per-split", type=int, default=16)
    parser.add_argument("--n-candidate-layers", type=int, default=4)
    parser.add_argument("--out-dir", default="artifacts/safe_mech")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = build_safe_mech_assay(args.n_per_split)
    validate_safe_mech_assay(rows)
    Path(out_dir / "safe_mech_assay.jsonl").write_text("\n".join(json.dumps(r, sort_keys=True) for r in rows) + "\n")

    fit_rows = [r for r in rows if r["split"] == "construct-fit" and r["policy"] in ("answer", "abstain")]
    dev_rows = [r for r in rows if r["split"] == "carrier-dev" and r["policy"] in ("answer", "abstain")]

    tokenizer, model = load_model(args.model, args.device, args.dtype)

    fit_grouped = collect_all_layer_means(model, tokenizer, fit_rows, args.device)
    dev_grouped = collect_all_layer_means(model, tokenizer, dev_rows, args.device)

    torch.save({"fit": fit_grouped, "dev": dev_grouped}, out_dir / "raw_layer_examples.pt")

    num_layers = model.config.num_hidden_layers
    layer_rows = []
    fit_example_vectors: dict[int, dict[str, torch.Tensor]] = {}
    for layer in range(num_layers):
        fit_cells = fit_grouped[layer]
        dev_cells = dev_grouped[layer]
        fit_means = cell_means_from_examples(fit_cells)
        contrasts = extract_contrasts(fit_means)
        p_direction = contrasts["p_contrast"]
        h_direction = contrasts["h_contrast"]
        dev_answer = dev_cells["h0_p0"] + dev_cells["h1_p0"]
        dev_abstain = dev_cells["h0_p1"] + dev_cells["h1_p1"]
        dev_astronomy = dev_cells["h0_p0"] + dev_cells["h0_p1"]
        dev_cooking = dev_cells["h1_p0"] + dev_cells["h1_p1"]
        p_separation_dev = project_separation(p_direction, dev_abstain, dev_answer)
        h_leakage_dev = project_separation(p_direction, dev_cooking, dev_astronomy)
        h_separation_dev = project_separation(h_direction, dev_cooking, dev_astronomy)
        p_leakage_on_h_direction = project_separation(h_direction, dev_abstain, dev_answer)
        layer_rows.append({
            "layer": layer,
            "raw_h_contrast_norm": float(contrasts["raw_h_contrast"].norm()),
            "raw_p_contrast_norm": float(contrasts["raw_p_contrast"].norm()),
            "h_p_cosine": cosine(contrasts["h_contrast"], contrasts["p_contrast"]),
            "p_separation_dev_effect_size": p_separation_dev,
            "h_leakage_on_p_direction_dev": h_leakage_dev,
            "h_separation_dev_effect_size": h_separation_dev,
            "p_leakage_on_h_direction_dev": p_leakage_on_h_direction,
        })
        fit_example_vectors[layer] = {"cells": fit_cells}

    csv_lines = ["layer,raw_h_contrast_norm,raw_p_contrast_norm,h_p_cosine,p_separation_dev_effect_size,h_leakage_on_p_direction_dev,h_separation_dev_effect_size,p_leakage_on_h_direction_dev"]
    for row in layer_rows:
        csv_lines.append(",".join(str(row[key]) for key in ["layer", "raw_h_contrast_norm", "raw_p_contrast_norm", "h_p_cosine", "p_separation_dev_effect_size", "h_leakage_on_p_direction_dev", "h_separation_dev_effect_size", "p_leakage_on_h_direction_dev"]))
    Path(out_dir / "safe_hxp_layer_scan.csv").write_text("\n".join(csv_lines) + "\n")

    ranked = sorted(layer_rows, key=lambda r: abs(r["p_separation_dev_effect_size"]) - abs(r["h_leakage_on_p_direction_dev"]), reverse=True)
    candidate_layers = [r["layer"] for r in ranked[: args.n_candidate_layers]]

    candidates = {}
    for layer in candidate_layers:
        fit_cells = fit_grouped[layer]
        stability = bootstrap_direction_stability(fit_cells, draws=200)
        loo_rows = fit_rows
        loo_vectors = {}
        for cell_key, tensors in fit_cells.items():
            h_part, p_part = cell_key.split("_")
            h_val = int(h_part[1:])
            p_val = int(p_part[1:])
            matching = [r for r in fit_rows if r["h"] == h_val and r["p"] == p_val]
            for row, tensor in zip(matching, tensors):
                loo_vectors[row["example_id"]] = tensor
        loo = leave_one_family_out_stability(loo_rows, loo_vectors)
        fit_means = cell_means_from_examples(fit_cells)
        contrasts = extract_contrasts(fit_means)
        candidates[str(layer)] = {
            "layer": layer,
            "p_direction": contrasts["p_contrast"].tolist(),
            "raw_p_contrast_norm": float(contrasts["raw_p_contrast"].norm()),
            "bootstrap_stability": stability,
            "leave_one_family_out_stability": loo,
            "dev_separation_effect_size": next(r["p_separation_dev_effect_size"] for r in layer_rows if r["layer"] == layer),
            "dev_h_leakage": next(r["h_leakage_on_p_direction_dev"] for r in layer_rows if r["layer"] == layer),
        }

    payload = {
        "role": "SAFE_MECH_BENIGN_PROXY",
        "model": args.model,
        "candidate_layers": candidate_layers,
        "selection_rule": "top-N by (|dev P separation effect size| - |dev H leakage|), computed only on construct-fit + carrier-dev",
        "candidates": candidates,
    }
    Path(out_dir / "safe_candidate_carriers.json").write_text(json.dumps(payload, indent=2))
    print(json.dumps({"candidate_layers": candidate_layers}, indent=2))


if __name__ == "__main__":
    main()
