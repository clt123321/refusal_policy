import argparse
import itertools
import json
from contextlib import ExitStack, contextmanager
from pathlib import Path

import torch

from src.data.safe_mech import build_safe_mech_assay, validate_safe_mech_assay
from src.eval.policy_classifier import classify_policy, is_compliant
from src.interventions.generation import steer_writer
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
    parser.add_argument("--raw-layers", default="artifacts/safe_mech/raw_layer_examples.pt")
    parser.add_argument("--out-dir", default="artifacts/safe_mech")
    parser.add_argument("--max-new-tokens", type=int, default=40)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_layers = torch.load(args.raw_layers)
    writers = [(20, "attn_output"), (24, "attn_output"), (27, "mlp_output"), (26, "mlp_output")]
    residual_directions = {layer: extract_contrasts(cell_means_from_examples(raw_layers["fit"][layer]))["p_contrast"] for layer, _ in writers}

    rows = build_safe_mech_assay(args.n_per_split)
    validate_safe_mech_assay(rows)
    test_rows = [r for r in rows if r["split"] == "carrier-test"]
    abstain_rows = [r for r in test_rows if r["policy"] == "abstain"]

    tokenizer, model = load_model(args.model, args.device, args.dtype)
    device = args.device

    baseline = run_condition(model, tokenizer, device, abstain_rows, None, args.max_new_tokens)

    def rate(results, key):
        return [1.0 if r[key] else 0.0 for r in results]

    def make_ctx(subset):
        @contextmanager
        def ctx():
            with ExitStack() as stack:
                for layer, module in subset:
                    stack.enter_context(steer_writer(model, layer, module, "remove", residual_directions[layer]))
                yield
        return ctx

    all_subsets = []
    for size in range(1, len(writers) + 1):
        all_subsets.extend(itertools.combinations(writers, size))

    summary_rows = []
    raw_records = [{"condition": "baseline", **r} for r in baseline]
    for subset in all_subsets:
        name = "+".join(f"L{l}_{m}" for l, m in subset)
        results = run_condition(model, tokenizer, device, abstain_rows, make_ctx(subset), args.max_new_tokens)
        raw_records += [{"condition": name, **r} for r in results]
        necessity = bootstrap_paired_diff(rate(results, "is_compliant"), rate(baseline, "is_compliant"))
        ontopic = sum(1 for r in results if r["label"] == "answer") / len(results)
        summary_rows.append({
            "subset": name,
            "size": len(subset),
            "necessity_effect_pp": necessity["mean_diff"] * 100,
            "necessity_ci_pp": [necessity["ci_low"] * 100, necessity["ci_high"] * 100],
            "ontopic_answer_rate": ontopic,
        })
        print(name, necessity["mean_diff"] * 100, necessity["ci_low"] * 100, necessity["ci_high"] * 100)

    Path(out_dir / "writer_subset_removal.json").write_text(json.dumps(summary_rows, indent=2))
    Path(out_dir / "raw_completions_writer_subsets.jsonl").write_text("\n".join(json.dumps(r) for r in raw_records) + "\n")
    csv_lines = ["subset,size,necessity_effect_pp,ci_low_pp,ci_high_pp,ontopic_answer_rate"]
    for row in summary_rows:
        csv_lines.append(f"{row['subset']},{row['size']},{row['necessity_effect_pp']},{row['necessity_ci_pp'][0]},{row['necessity_ci_pp'][1]},{row['ontopic_answer_rate']}")
    Path(out_dir / "writer_subset_removal.csv").write_text("\n".join(csv_lines) + "\n")


if __name__ == "__main__":
    main()
