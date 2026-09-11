import argparse
import json
from pathlib import Path

import torch

from src.data.safe_mech import build_safe_mech_assay, validate_safe_mech_assay
from src.eval.policy_classifier import classify_policy, is_compliant
from src.models.runtime import encode, layer_modules, load_model
from src.stats.contrasts import cell_means_from_examples, extract_contrasts, cosine as cosine_fn

ABSTAIN_TOKEN = " I"
ANSWER_TOKEN = " The"


def get_last_token(hidden, attention_mask):
    idx = attention_mask.sum(dim=1).long() - 1
    return hidden[torch.arange(hidden.shape[0], device=hidden.device), idx]


def capture_baseline(model, tokenizer, device, prompt, layer_index):
    encoded = encode(tokenizer, [prompt], device)
    captured = {}
    layer = layer_modules(model)[layer_index]

    def mlp_hook(_m, _inp, output):
        hidden = output[0] if isinstance(output, tuple) else output
        captured["mlp_output"] = hidden.detach()

    def layer_hook(_m, _inp, output):
        hidden = output[0] if isinstance(output, tuple) else output
        captured["block_residual"] = hidden.detach()

    def norm_hook(_m, _inp, output):
        captured["normed"] = output.detach()

    h1 = layer.mlp.register_forward_hook(mlp_hook)
    h2 = layer.register_forward_hook(layer_hook)
    h3 = model.model.norm.register_forward_hook(norm_hook)
    try:
        with torch.no_grad():
            outputs = model(**encoded, use_cache=False)
    finally:
        h1.remove(); h2.remove(); h3.remove()
    return {
        "mlp_output": get_last_token(captured["mlp_output"], encoded["attention_mask"])[0],
        "block_residual": get_last_token(captured["block_residual"], encoded["attention_mask"])[0],
        "normed": get_last_token(captured["normed"], encoded["attention_mask"])[0],
        "logits": get_last_token(outputs.logits, encoded["attention_mask"])[0],
    }, encoded


def forward_overwrite_at(model, tokenizer, device, prompt, hook_module_getter, delta, is_norm_locus=False):
    encoded = encode(tokenizer, [prompt], device)
    module = hook_module_getter(model)
    captured = {}

    def hook(_m, _inp, output):
        is_tuple = isinstance(output, tuple)
        hidden = output[0] if is_tuple else output
        idx = encoded["attention_mask"].sum(dim=1).long() - 1
        new_hidden = hidden.clone()
        new_hidden[torch.arange(hidden.shape[0], device=hidden.device), idx] = hidden[torch.arange(hidden.shape[0], device=hidden.device), idx] + delta.to(hidden.dtype)
        captured["result"] = new_hidden.detach()
        if is_tuple:
            return (new_hidden,) + output[1:]
        return new_hidden

    handle = module.register_forward_hook(hook)
    norm_capture = {}
    h_norm = None
    if not is_norm_locus:
        def norm_hook(_m, _inp, output):
            norm_capture["normed"] = output.detach()
        h_norm = model.model.norm.register_forward_hook(norm_hook)
    try:
        with torch.no_grad():
            outputs = model(**encoded, use_cache=False)
    finally:
        handle.remove()
        if h_norm is not None:
            h_norm.remove()
    logits = get_last_token(outputs.logits, encoded["attention_mask"])[0]
    if is_norm_locus:
        normed = get_last_token(captured["result"], encoded["attention_mask"])[0]
    else:
        normed = get_last_token(norm_capture["normed"], encoded["attention_mask"])[0]
    perturbed_state = get_last_token(captured["result"], encoded["attention_mask"])[0]
    return {"logits": logits, "normed": normed, "perturbed_state": perturbed_state}


def generate_with_overwrite(model, tokenizer, device, prompt, hook_module_getter, delta, is_norm_locus, max_new_tokens=40):
    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt").to(device)
    module = hook_module_getter(model)

    def hook(_m, _inp, output):
        is_tuple = isinstance(output, tuple)
        hidden = output[0] if is_tuple else output
        new_hidden = hidden + delta.to(hidden.dtype)
        if is_tuple:
            return (new_hidden,) + output[1:]
        return new_hidden

    handle = module.register_forward_hook(hook)
    try:
        with torch.inference_mode():
            out = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False, pad_token_id=tokenizer.pad_token_id)
    finally:
        handle.remove()
    return tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="Qwen/Qwen2.5-1.5B-Instruct")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--layer", type=int, default=27)
    parser.add_argument("--n-per-split", type=int, default=16)
    parser.add_argument("--n-examples", type=int, default=8)
    parser.add_argument("--raw-layers", default="artifacts/safe_mech/raw_layer_examples.pt")
    parser.add_argument("--out-dir", default="artifacts/safe_mech")
    parser.add_argument("--max-new-tokens", type=int, default=40)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_layers = torch.load(args.raw_layers)
    direction = extract_contrasts(cell_means_from_examples(raw_layers["fit"][args.layer]))["p_contrast"]
    unit = direction / direction.norm()

    rows = build_safe_mech_assay(args.n_per_split)
    validate_safe_mech_assay(rows)
    abstain_rows = [r for r in rows if r["split"] == "carrier-test" and r["policy"] == "abstain"][: args.n_examples]

    tokenizer, model = load_model(args.model, args.device, "float32")
    device = args.device
    abstain_id = tokenizer.encode(ABSTAIN_TOKEN, add_special_tokens=False)[0]
    answer_id = tokenizer.encode(ANSWER_TOKEN, add_special_tokens=False)[0]

    layer_module = lambda m: layer_modules(m)[args.layer].mlp
    layer_out_module = lambda m: layer_modules(m)[args.layer]
    norm_module = lambda m: m.model.norm

    rows_out = []
    for row in abstain_rows:
        baseline, encoded = capture_baseline(model, tokenizer, device, row["prompt"], args.layer)
        unit_dev = unit.to(device)
        delta_mlp = -torch.dot(baseline["mlp_output"], unit_dev) * unit_dev

        a = forward_overwrite_at(model, tokenizer, device, row["prompt"], layer_module, delta_mlp, is_norm_locus=False)
        b = forward_overwrite_at(model, tokenizer, device, row["prompt"], layer_out_module, delta_mlp, is_norm_locus=False)
        c = forward_overwrite_at(model, tokenizer, device, row["prompt"], norm_module, delta_mlp, is_norm_locus=True)

        gen_a = generate_with_overwrite(model, tokenizer, device, row["prompt"], layer_module, delta_mlp, False, args.max_new_tokens)
        gen_b = generate_with_overwrite(model, tokenizer, device, row["prompt"], layer_out_module, delta_mlp, False, args.max_new_tokens)
        gen_c = generate_with_overwrite(model, tokenizer, device, row["prompt"], norm_module, delta_mlp, True, args.max_new_tokens)

        for name, result, gen_text in [("A_mlp_output", a, gen_a), ("B_residual_pre_norm", b, gen_b), ("C_post_norm", c, gen_c)]:
            label = classify_policy(gen_text, row["topic"])
            rows_out.append({
                "example_id": row["example_id"],
                "locus": name,
                "delta_norm": float(delta_mlp.norm()),
                "perturbed_state_norm": float(result["perturbed_state"].norm()),
                "cosine_to_baseline_normed": cosine_fn(result["normed"], baseline["normed"]),
                "policy_logit_margin": float(result["logits"][abstain_id] - result["logits"][answer_id]),
                "baseline_policy_logit_margin": float(baseline["logits"][abstain_id] - baseline["logits"][answer_id]),
                "behavior_label": label,
                "is_abstain": label == "abstain",
                "is_compliant": is_compliant(label),
            })

    Path(out_dir / "normalization_localization.json").write_text(json.dumps(rows_out, indent=2))
    csv_lines = ["example_id,locus,delta_norm,perturbed_state_norm,cosine_to_baseline_normed,policy_logit_margin,baseline_policy_logit_margin,behavior_label,is_abstain,is_compliant"]
    for r in rows_out:
        csv_lines.append(",".join(str(r[k]) for k in ["example_id", "locus", "delta_norm", "perturbed_state_norm", "cosine_to_baseline_normed", "policy_logit_margin", "baseline_policy_logit_margin", "behavior_label", "is_abstain", "is_compliant"]))
    Path(out_dir / "normalization_localization.csv").write_text("\n".join(csv_lines) + "\n")

    for locus in ["A_mlp_output", "B_residual_pre_norm", "C_post_norm"]:
        sub = [r for r in rows_out if r["locus"] == locus]
        print(locus, "abstain_rate=", sum(r["is_abstain"] for r in sub) / len(sub), "mean_margin=", sum(r["policy_logit_margin"] for r in sub) / len(sub))


if __name__ == "__main__":
    main()
