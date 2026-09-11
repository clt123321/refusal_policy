import argparse
import json
from pathlib import Path

import torch

from src.data.safe_mech import build_safe_mech_assay, validate_safe_mech_assay
from src.eval.policy_classifier import classify_policy, is_compliant
from src.interventions.generation import steer_multi_layer
from src.interventions.proxy import norm_matched_random, orthogonal_random
from src.models.runtime import load_model
from src.stats.contrasts import bootstrap_mean, bootstrap_paired_diff, cell_means_from_examples, extract_contrasts, shuffled_label_cells


def generate_one(model, tokenizer, device, prompt: str, max_new_tokens: int = 40) -> str:
    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt").to(device)
    with torch.inference_mode():
        out = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False, pad_token_id=tokenizer.pad_token_id)
    return tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)


def run_condition(model, tokenizer, device, rows, ctx_factory, max_new_tokens: int = 40):
    results = []
    for row in rows:
        if ctx_factory is None:
            completion = generate_one(model, tokenizer, device, row["prompt"], max_new_tokens)
        else:
            with ctx_factory():
                completion = generate_one(model, tokenizer, device, row["prompt"], max_new_tokens)
        label = classify_policy(completion, row["topic"])
        results.append({"example_id": row["example_id"], "topic": row["topic"], "completion": completion, "label": label, "is_abstain": label == "abstain", "is_compliant": is_compliant(label)})
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="Qwen/Qwen2.5-1.5B-Instruct")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--dtype", default="float16")
    parser.add_argument("--n-per-split", type=int, default=16)
    parser.add_argument("--ablation-start", type=int, default=18)
    parser.add_argument("--ablation-end", type=int, default=23)
    parser.add_argument("--wrong-layer-shift", type=int, default=-12)
    parser.add_argument("--raw-layers", default="artifacts/safe_mech/raw_layer_examples.pt")
    parser.add_argument("--out-dir", default="artifacts/safe_mech")
    parser.add_argument("--max-new-tokens", type=int, default=40)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_layers = torch.load(args.raw_layers)
    ablation_layers = list(range(args.ablation_start, args.ablation_end + 1))

    true_directions, true_alphas, h_directions, shuffled_directions, shuffled_alphas = {}, {}, {}, {}, {}
    for layer in ablation_layers:
        cells = raw_layers["fit"][layer]
        means = cell_means_from_examples(cells)
        contrasts = extract_contrasts(means)
        true_directions[layer] = contrasts["p_contrast"]
        true_alphas[layer] = float(contrasts["raw_p_contrast"].norm())
        h_directions[layer] = contrasts["h_contrast"]
        shuffled_cells = shuffled_label_cells(cells, seed=100 + layer)
        shuffled_means = cell_means_from_examples(shuffled_cells)
        shuffled_contrasts = extract_contrasts(shuffled_means)
        shuffled_directions[layer] = shuffled_contrasts["p_contrast"]

    random_directions = {layer: norm_matched_random(true_directions[layer], seed=200 + layer) for layer in ablation_layers}
    orthogonal_directions = {layer: orthogonal_random(true_directions[layer], seed=300 + layer) for layer in ablation_layers}
    wrong_layer_targets = {layer + args.wrong_layer_shift: true_directions[layer] for layer in ablation_layers}
    wrong_layer_alphas = {layer + args.wrong_layer_shift: true_alphas[layer] for layer in ablation_layers}

    controls = {
        "random_norm_matched": (true_directions.keys(), random_directions, true_alphas, False),
        "orthogonal": (true_directions.keys(), orthogonal_directions, true_alphas, False),
        "h_content_direction": (true_directions.keys(), h_directions, true_alphas, False),
        "shuffled_label": (true_directions.keys(), shuffled_directions, true_alphas, False),
        "wrong_layer": (wrong_layer_targets.keys(), wrong_layer_targets, wrong_layer_alphas, False),
        "wrong_token": (true_directions.keys(), true_directions, true_alphas, True),
    }

    rows = build_safe_mech_assay(args.n_per_split)
    validate_safe_mech_assay(rows)
    test_rows = [r for r in rows if r["split"] == "carrier-test"]
    abstain_rows = [r for r in test_rows if r["policy"] == "abstain"]
    natural_rows = [r for r in test_rows if r["policy"] == "natural"]

    tokenizer, model = load_model(args.model, args.device, args.dtype)
    device = args.device

    baseline_abstain = run_condition(model, tokenizer, device, abstain_rows, None, args.max_new_tokens)
    baseline_natural = run_condition(model, tokenizer, device, natural_rows, None, args.max_new_tokens)

    summary_rows = []
    raw_records = [{"condition": "baseline_abstain", **r} for r in baseline_abstain] + [{"condition": "baseline_natural", **r} for r in baseline_natural]

    def rate(results, key):
        return [1.0 if r[key] else 0.0 for r in results]

    for name, (layer_keys, directions, alphas, first_token_only) in controls.items():
        layer_dirs = {layer: directions[layer] for layer in layer_keys}
        layer_alphas = {layer: alphas[layer] for layer in layer_keys}

        def remove_ctx(ld=layer_dirs, fto=first_token_only):
            return steer_multi_layer(model, "remove", ld, first_token_only=fto)

        def add_ctx(ld=layer_dirs, la=layer_alphas, fto=first_token_only):
            return steer_multi_layer(model, "add", ld, la, first_token_only=fto)

        remove_results = run_condition(model, tokenizer, device, abstain_rows, remove_ctx, args.max_new_tokens)
        add_results = run_condition(model, tokenizer, device, natural_rows, add_ctx, args.max_new_tokens)
        raw_records += [{"condition": f"{name}_remove", **r} for r in remove_results]
        raw_records += [{"condition": f"{name}_add", **r} for r in add_results]

        necessity = bootstrap_paired_diff(rate(remove_results, "is_compliant"), rate(baseline_abstain, "is_compliant"))
        sufficiency = bootstrap_paired_diff(rate(add_results, "is_abstain"), rate(baseline_natural, "is_abstain"))
        summary_rows.append({
            "control": name,
            "necessity_effect_pp": necessity["mean_diff"] * 100,
            "necessity_ci_pp": [necessity["ci_low"] * 100, necessity["ci_high"] * 100],
            "sufficiency_effect_pp": sufficiency["mean_diff"] * 100,
            "sufficiency_ci_pp": [sufficiency["ci_low"] * 100, sufficiency["ci_high"] * 100],
        })

    Path(out_dir / "raw_completions_controls.jsonl").write_text("\n".join(json.dumps(r) for r in raw_records) + "\n")
    Path(out_dir / "safe_negative_controls.json").write_text(json.dumps(summary_rows, indent=2))

    csv_lines = ["control,necessity_effect_pp,necessity_ci_low_pp,necessity_ci_high_pp,sufficiency_effect_pp,sufficiency_ci_low_pp,sufficiency_ci_high_pp"]
    for row in summary_rows:
        csv_lines.append(f"{row['control']},{row['necessity_effect_pp']},{row['necessity_ci_pp'][0]},{row['necessity_ci_pp'][1]},{row['sufficiency_effect_pp']},{row['sufficiency_ci_pp'][0]},{row['sufficiency_ci_pp'][1]}")
    Path(out_dir / "safe_negative_controls.csv").write_text("\n".join(csv_lines) + "\n")

    print(json.dumps(summary_rows, indent=2))


if __name__ == "__main__":
    main()
