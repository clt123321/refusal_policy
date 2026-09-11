import argparse
import json
from pathlib import Path

import torch

from src.data.safe_mech import build_safe_mech_assay, validate_safe_mech_assay
from src.eval.policy_classifier import classify_policy, is_compliant
from src.interventions.generation import steer_writer
from src.models.runtime import encode, load_model
from src.stats.contrasts import bootstrap_mean, cell_means_from_examples, extract_contrasts

ABSTAIN_TOKEN = " I"
ANSWER_TOKEN = " The"


def get_last_token(hidden, attention_mask):
    idx = attention_mask.sum(dim=1).long() - 1
    return hidden[torch.arange(hidden.shape[0], device=hidden.device), idx]


def logit_margin(model, tokenizer, device, prompt, layer_index, direction, alpha, abstain_id, answer_id):
    encoded = encode(tokenizer, [prompt], device)
    if alpha == 0.0:
        with torch.no_grad():
            outputs = model(**encoded, use_cache=False)
    else:
        with steer_writer(model, layer_index, "mlp_output", "scale", direction, alpha=alpha):
            with torch.no_grad():
                outputs = model(**encoded, use_cache=False)
    last_logits = get_last_token(outputs.logits, encoded["attention_mask"])[0]
    return float(last_logits[abstain_id] - last_logits[answer_id])


def generate_one(model, tokenizer, device, prompt, layer_index, direction, alpha, max_new_tokens=40):
    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt").to(device)
    if alpha == 0.0:
        with torch.inference_mode():
            out = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False, pad_token_id=tokenizer.pad_token_id)
    else:
        with steer_writer(model, layer_index, "mlp_output", "scale", direction, alpha=alpha):
            with torch.inference_mode():
                out = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False, pad_token_id=tokenizer.pad_token_id)
    return tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="Qwen/Qwen2.5-1.5B-Instruct")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--dtype", default="float16")
    parser.add_argument("--layer", type=int, default=27)
    parser.add_argument("--n-per-split", type=int, default=16)
    parser.add_argument("--raw-layers", default="artifacts/safe_mech/raw_layer_examples.pt")
    parser.add_argument("--out-dir", default="artifacts/safe_mech")
    parser.add_argument("--max-new-tokens", type=int, default=40)
    parser.add_argument("--alphas", default="-2,-1.5,-1,-0.5,0,0.5,1,1.5,2")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_layers = torch.load(args.raw_layers)
    direction = extract_contrasts(cell_means_from_examples(raw_layers["fit"][args.layer]))["p_contrast"]
    alphas = [float(x) for x in args.alphas.split(",")]

    rows = build_safe_mech_assay(args.n_per_split)
    validate_safe_mech_assay(rows)
    test_rows = [r for r in rows if r["split"] == "carrier-test"]
    abstain_rows = [r for r in test_rows if r["policy"] == "abstain"]

    tokenizer, model = load_model(args.model, args.device, args.dtype)
    device = args.device
    abstain_id = tokenizer.encode(ABSTAIN_TOKEN, add_special_tokens=False)[0]
    answer_id = tokenizer.encode(ANSWER_TOKEN, add_special_tokens=False)[0]

    rows_out = []
    raw_records = []
    for alpha in alphas:
        margins = []
        behaviors = []
        for row in abstain_rows:
            margin = logit_margin(model, tokenizer, device, row["prompt"], args.layer, direction, alpha, abstain_id, answer_id)
            completion = generate_one(model, tokenizer, device, row["prompt"], args.layer, direction, alpha, args.max_new_tokens)
            label = classify_policy(completion, row["topic"])
            margins.append(margin)
            behaviors.append({"is_abstain": label == "abstain", "is_compliant": is_compliant(label), "label": label})
            raw_records.append({"alpha": alpha, "example_id": row["example_id"], "logit_margin": margin, "completion": completion, "label": label})
        n = len(behaviors)
        abstain_rate = sum(b["is_abstain"] for b in behaviors) / n
        compliant_rate = sum(b["is_compliant"] for b in behaviors) / n
        invalid_rate = sum(1 for b in behaviors if b["label"] == "invalid") / n
        margin_stats = bootstrap_mean(margins)
        rows_out.append({
            "alpha": alpha,
            "abstain_rate": abstain_rate,
            "compliant_rate": compliant_rate,
            "invalid_rate": invalid_rate,
            "mean_logit_margin": margin_stats["mean"],
            "logit_margin_ci_low": margin_stats["ci_low"],
            "logit_margin_ci_high": margin_stats["ci_high"],
        })
        print(alpha, rows_out[-1])

    Path(out_dir / "l27_dose_response.csv").write_text(
        "alpha,abstain_rate,compliant_rate,invalid_rate,mean_logit_margin,logit_margin_ci_low,logit_margin_ci_high\n"
        + "\n".join(f"{r['alpha']},{r['abstain_rate']},{r['compliant_rate']},{r['invalid_rate']},{r['mean_logit_margin']},{r['logit_margin_ci_low']},{r['logit_margin_ci_high']}" for r in rows_out)
        + "\n"
    )
    Path(out_dir / "l27_dose_response.json").write_text(json.dumps(rows_out, indent=2))
    Path(out_dir / "raw_completions_dose_response.jsonl").write_text("\n".join(json.dumps(r) for r in raw_records) + "\n")


if __name__ == "__main__":
    main()
