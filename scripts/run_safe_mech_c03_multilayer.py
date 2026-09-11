import argparse
import json
from pathlib import Path

import torch

from src.data.safe_mech import build_safe_mech_assay, validate_safe_mech_assay
from src.eval.policy_classifier import classify_policy, is_compliant
from src.interventions.generation import steer_multi_layer, steer_multi_remove_then_patch
from src.models.runtime import load_model
from src.stats.contrasts import bootstrap_mean, bootstrap_paired_diff, cell_means_from_examples, extract_contrasts


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
        results.append({"example_id": row["example_id"], "topic": row["topic"], "family": row["family"], "completion": completion, "label": label, "is_abstain": label == "abstain", "is_compliant": is_compliant(label)})
    return results


def layer_direction_and_alpha(raw_layers: dict, split: str, layer: int) -> tuple[torch.Tensor, float]:
    cells = raw_layers[split][layer]
    means = cell_means_from_examples(cells)
    contrasts = extract_contrasts(means)
    return contrasts["p_contrast"], float(contrasts["raw_p_contrast"].norm())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="Qwen/Qwen2.5-1.5B-Instruct")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--dtype", default="float16")
    parser.add_argument("--n-per-split", type=int, default=16)
    parser.add_argument("--ablation-start", type=int, default=18)
    parser.add_argument("--ablation-end", type=int, default=23, help="inclusive")
    parser.add_argument("--patch-layer", type=int, default=26)
    parser.add_argument("--raw-layers", default="artifacts/safe_mech/raw_layer_examples.pt")
    parser.add_argument("--out-dir", default="artifacts/safe_mech")
    parser.add_argument("--max-new-tokens", type=int, default=40)
    parser.add_argument("--tag", default="multilayer")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_layers = torch.load(args.raw_layers)
    ablation_layers = list(range(args.ablation_start, args.ablation_end + 1))
    fit_directions = {}
    fit_alphas = {}
    for layer in ablation_layers:
        direction, alpha = layer_direction_and_alpha(raw_layers, "fit", layer)
        fit_directions[layer] = direction
        fit_alphas[layer] = alpha
    patch_direction, patch_alpha = layer_direction_and_alpha(raw_layers, "fit", args.patch_layer)

    rows = build_safe_mech_assay(args.n_per_split)
    validate_safe_mech_assay(rows)
    test_rows = [r for r in rows if r["split"] == "carrier-test"]
    abstain_rows = [r for r in test_rows if r["policy"] == "abstain"]
    answer_rows = [r for r in test_rows if r["policy"] == "answer"]
    natural_rows = [r for r in test_rows if r["policy"] == "natural"]

    tokenizer, model = load_model(args.model, args.device, args.dtype)
    device = args.device

    def remove_ctx():
        return steer_multi_layer(model, "remove", fit_directions)

    def add_ctx():
        return steer_multi_layer(model, "add", fit_directions, fit_alphas)

    def rescue_ctx():
        return steer_multi_remove_then_patch(model, fit_directions, args.patch_layer, patch_direction, patch_alpha)

    conditions = {
        "baseline_abstain": (abstain_rows, None),
        "remove": (abstain_rows, remove_ctx),
        "rescue": (abstain_rows, rescue_ctx),
        "baseline_answer": (answer_rows, None),
        "baseline_natural": (natural_rows, None),
        "add": (natural_rows, add_ctx),
    }

    all_results = {}
    for name, (condition_rows, ctx) in conditions.items():
        all_results[name] = run_condition(model, tokenizer, device, condition_rows, ctx, args.max_new_tokens)

    raw_path = out_dir / f"raw_completions_{args.tag}.jsonl"
    with raw_path.open("w") as f:
        for condition, results in all_results.items():
            for r in results:
                f.write(json.dumps({"condition": condition, **r}) + "\n")

    def rate(results, key):
        return [1.0 if r[key] else 0.0 for r in results]

    necessity = bootstrap_paired_diff(rate(all_results["remove"], "is_compliant"), rate(all_results["baseline_abstain"], "is_compliant"))
    sufficiency = bootstrap_paired_diff(rate(all_results["add"], "is_abstain"), rate(all_results["baseline_natural"], "is_abstain"))
    baseline_abstain_rate = bootstrap_mean(rate(all_results["baseline_abstain"], "is_abstain"))
    remove_abstain_rate = bootstrap_mean(rate(all_results["remove"], "is_abstain"))
    rescue_abstain_rate = bootstrap_mean(rate(all_results["rescue"], "is_abstain"))
    denom = baseline_abstain_rate["mean"] - remove_abstain_rate["mean"]
    rescue_fraction = (rescue_abstain_rate["mean"] - remove_abstain_rate["mean"]) / denom if abs(denom) > 1e-9 else float("nan")

    summary = {
        "role": "SAFE_MECH_BENIGN_PROXY",
        "ablation_layers": ablation_layers,
        "patch_layer": args.patch_layer,
        "necessity_effect_pp": necessity["mean_diff"] * 100,
        "necessity_ci_pp": [necessity["ci_low"] * 100, necessity["ci_high"] * 100],
        "sufficiency_effect_pp": sufficiency["mean_diff"] * 100,
        "sufficiency_ci_pp": [sufficiency["ci_low"] * 100, sufficiency["ci_high"] * 100],
        "baseline_abstain_rate": baseline_abstain_rate,
        "remove_abstain_rate": remove_abstain_rate,
        "rescue_abstain_rate": rescue_abstain_rate,
        "rescue_fraction": rescue_fraction,
        "baseline_answer_ontopic_rate": bootstrap_mean([1.0 if r["label"] == "answer" else 0.0 for r in all_results["baseline_answer"]]),
        "baseline_natural_ontopic_rate": bootstrap_mean([1.0 if r["label"] == "answer" else 0.0 for r in all_results["baseline_natural"]]),
    }
    Path(out_dir / f"causal_policy_intervention_{args.tag}.json").write_text(json.dumps(summary, indent=2))

    csv_lines = ["condition,n,abstain_rate,compliant_rate,ontopic_answer_rate"]
    for name, results in all_results.items():
        n = len(results)
        csv_lines.append(f"{name},{n},{sum(r['is_abstain'] for r in results)/n},{sum(r['is_compliant'] for r in results)/n},{sum(1 for r in results if r['label']=='answer')/n}")
    Path(out_dir / f"causal_policy_intervention_{args.tag}.csv").write_text("\n".join(csv_lines) + "\n")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
