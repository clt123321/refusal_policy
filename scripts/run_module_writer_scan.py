import argparse
import json
from pathlib import Path

import torch

from src.data.safe_mech import build_safe_mech_assay, validate_safe_mech_assay
from src.eval.policy_classifier import classify_policy, is_compliant
from src.hooks.multi_capture import collect_writer_means
from src.interventions.generation import steer_writer
from src.models.runtime import load_model
from src.stats.contrasts import bootstrap_mean, bootstrap_paired_diff, cell_means_from_examples, extract_contrasts


def writer_score(cells: dict[str, list[torch.Tensor]], residual_direction: torch.Tensor) -> float:
    means = cell_means_from_examples(cells)
    answer_mean = 0.5 * (means["h0_p0"] + means["h1_p0"])
    abstain_mean = 0.5 * (means["h0_p1"] + means["h1_p1"])
    diff = abstain_mean - answer_mean
    unit = residual_direction / residual_direction.norm()
    return float(torch.dot(diff, unit))


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
    parser.add_argument("--num-layers", type=int, default=28)
    parser.add_argument("--top-k-per-module", type=int, default=4)
    parser.add_argument("--raw-layers", default="artifacts/safe_mech/raw_layer_examples.pt")
    parser.add_argument("--out-dir", default="artifacts/safe_mech")
    parser.add_argument("--max-new-tokens", type=int, default=40)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_layers = torch.load(args.raw_layers)
    residual_directions = {layer: extract_contrasts(cell_means_from_examples(raw_layers["fit"][layer]))["p_contrast"] for layer in range(args.num_layers)}

    rows = build_safe_mech_assay(args.n_per_split)
    validate_safe_mech_assay(rows)
    fit_rows = [r for r in rows if r["split"] == "construct-fit" and r["policy"] in ("answer", "abstain")]
    test_rows = [r for r in rows if r["split"] == "carrier-test"]
    abstain_rows = [r for r in test_rows if r["policy"] == "abstain"]

    tokenizer, model = load_model(args.model, args.device, args.dtype)
    device = args.device

    writer_means = collect_writer_means(model, tokenizer, fit_rows, list(range(args.num_layers)), device)
    scores = {key: writer_score(cells, residual_directions[key[0]]) for key, cells in writer_means.items()}

    attn_ranked = sorted([k for k in scores if k[1] == "attn_output"], key=lambda k: abs(scores[k]), reverse=True)
    mlp_ranked = sorted([k for k in scores if k[1] == "mlp_output"], key=lambda k: abs(scores[k]), reverse=True)
    candidates = attn_ranked[: args.top_k_per_module] + mlp_ranked[: args.top_k_per_module]

    baseline = run_condition(model, tokenizer, device, abstain_rows, None, args.max_new_tokens)

    def rate(results, key):
        return [1.0 if r[key] else 0.0 for r in results]

    csv_lines = ["layer,module,projection_strength,single_removal_necessity_pp,necessity_ci_low_pp,necessity_ci_high_pp,ontopic_answer_rate"]
    raw_records = [{"condition": "baseline", **r} for r in baseline]
    per_writer_results = {}

    for layer, module in candidates:
        def ctx(l=layer, m=module):
            return steer_writer(model, l, m, "remove", residual_directions[l])

        results = run_condition(model, tokenizer, device, abstain_rows, ctx, args.max_new_tokens)
        raw_records += [{"condition": f"L{layer}_{module}", **r} for r in results]
        per_writer_results[(layer, module)] = results
        necessity = bootstrap_paired_diff(rate(results, "is_compliant"), rate(baseline, "is_compliant"))
        ontopic = sum(1 for r in results if r["label"] == "answer") / len(results)
        csv_lines.append(f"{layer},{module},{scores[(layer, module)]},{necessity['mean_diff'] * 100},{necessity['ci_low'] * 100},{necessity['ci_high'] * 100},{ontopic}")

    Path(out_dir / "module_writer_scan.csv").write_text("\n".join(csv_lines) + "\n")
    Path(out_dir / "module_writer_scores_all.json").write_text(json.dumps({f"L{k[0]}_{k[1]}": v for k, v in scores.items()}, indent=2))
    Path(out_dir / "raw_completions_writer_scan.jsonl").write_text("\n".join(json.dumps(r) for r in raw_records) + "\n")
    torch.save({"candidates": candidates, "writer_means": writer_means, "scores": scores}, out_dir / "writer_scan_state.pt")
    print("candidates:", candidates)
    print(open(out_dir / "module_writer_scan.csv").read())


if __name__ == "__main__":
    main()
