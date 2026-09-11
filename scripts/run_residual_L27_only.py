import argparse
import json
from pathlib import Path

import torch

from src.data.safe_mech import build_safe_mech_assay, validate_safe_mech_assay
from src.eval.policy_classifier import classify_policy, is_compliant
from src.interventions.generation import steer_layer
from src.models.runtime import load_model
from src.stats.contrasts import bootstrap_mean, bootstrap_paired_diff, cell_means_from_examples, extract_contrasts


def generate_one(model, tokenizer, device, prompt, max_new_tokens=40):
    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt").to(device)
    with torch.inference_mode():
        out = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False, pad_token_id=tokenizer.pad_token_id)
    return tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)


def run_condition(model, tokenizer, device, rows, ctx_factory, max_new_tokens=40):
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
    parser.add_argument("--layer", type=int, default=27)
    parser.add_argument("--raw-layers", default="artifacts/safe_mech/raw_layer_examples.pt")
    parser.add_argument("--out-dir", default="artifacts/safe_mech")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    raw_layers = torch.load(args.raw_layers)
    direction = extract_contrasts(cell_means_from_examples(raw_layers["fit"][args.layer]))["p_contrast"]

    rows = build_safe_mech_assay(args.n_per_split)
    validate_safe_mech_assay(rows)
    test_rows = [r for r in rows if r["split"] == "carrier-test"]
    abstain_rows = [r for r in test_rows if r["policy"] == "abstain"]

    tokenizer, model = load_model(args.model, args.device, args.dtype)
    device = args.device

    baseline = run_condition(model, tokenizer, device, abstain_rows, None)

    def ctx():
        return steer_layer(model, args.layer, "remove", direction)

    removed = run_condition(model, tokenizer, device, abstain_rows, ctx)

    def rate(results, key):
        return [1.0 if r[key] else 0.0 for r in results]

    necessity = bootstrap_paired_diff(rate(removed, "is_compliant"), rate(baseline, "is_compliant"))
    summary = {
        "role": "SAFE_MECH_BENIGN_PROXY",
        "layer": args.layer,
        "necessity_effect_pp": necessity["mean_diff"] * 100,
        "necessity_ci_pp": [necessity["ci_low"] * 100, necessity["ci_high"] * 100],
        "baseline_abstain_rate": bootstrap_mean(rate(baseline, "is_abstain")),
        "removed_abstain_rate": bootstrap_mean(rate(removed, "is_abstain")),
    }
    Path(out_dir / f"residual_removal_L{args.layer}_only.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
