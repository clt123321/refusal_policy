import argparse
import json
from pathlib import Path

import torch

from src.data.safe_mech import build_safe_mech_assay, validate_safe_mech_assay
from src.interventions.generation import steer_layer, steer_writer
from src.models.runtime import encode, layer_modules, load_model
from src.stats.contrasts import cell_means_from_examples, extract_contrasts


def get_last_token(hidden, attention_mask):
    idx = attention_mask.sum(dim=1).long() - 1
    return hidden[torch.arange(hidden.shape[0], device=hidden.device), idx]


def capture_forward(model, tokenizer, device, prompt, layer_index):
    encoded = encode(tokenizer, [prompt], device)
    captured = {}
    layer = layer_modules(model)[layer_index]

    def mlp_hook(_m, _inp, output):
        hidden = output[0] if isinstance(output, tuple) else output
        captured["mlp_output"] = hidden.detach()

    def mlp_pre_hook(_m, inputs):
        captured["mlp_input"] = inputs[0].detach()

    def layer_hook(_m, _inp, output):
        hidden = output[0] if isinstance(output, tuple) else output
        captured["block_residual"] = hidden.detach()

    h1 = layer.mlp.register_forward_pre_hook(mlp_pre_hook)
    h2 = layer.mlp.register_forward_hook(mlp_hook)
    h3 = layer.register_forward_hook(layer_hook)
    try:
        with torch.no_grad():
            outputs = model(**encoded, use_cache=False, output_hidden_states=False)
    finally:
        h1.remove(); h2.remove(); h3.remove()
    logits = outputs.logits
    last_logits = get_last_token(logits, encoded["attention_mask"])[0]
    normed = model.model.norm(captured["block_residual"])
    normed_last = get_last_token(normed, encoded["attention_mask"])[0]
    return {
        "mlp_input": get_last_token(captured["mlp_input"], encoded["attention_mask"])[0],
        "mlp_output": get_last_token(captured["mlp_output"], encoded["attention_mask"])[0],
        "block_residual": get_last_token(captured["block_residual"], encoded["attention_mask"])[0],
        "normed": normed_last,
        "logits": last_logits,
    }, encoded


def forward_with_mlp_removal(model, tokenizer, device, prompt, layer_index, direction):
    encoded = encode(tokenizer, [prompt], device)
    captured = {}
    layer = layer_modules(model)[layer_index]

    def layer_hook(_m, _inp, output):
        hidden = output[0] if isinstance(output, tuple) else output
        captured["block_residual"] = hidden.detach()

    h_layer = layer.register_forward_hook(layer_hook)
    try:
        with steer_writer(model, layer_index, "mlp_output", "remove", direction):
            with torch.no_grad():
                outputs = model(**encoded, use_cache=False)
    finally:
        h_layer.remove()
    logits = get_last_token(outputs.logits, encoded["attention_mask"])[0]
    normed = get_last_token(model.model.norm(captured["block_residual"]), encoded["attention_mask"])[0]
    residual = get_last_token(captured["block_residual"], encoded["attention_mask"])[0]
    return {"block_residual": residual, "normed": normed, "logits": logits}


def forward_with_residual_overwrite(model, tokenizer, device, prompt, layer_index, target_last_token_value):
    encoded = encode(tokenizer, [prompt], device)
    layer = layer_modules(model)[layer_index]
    captured = {}

    def overwrite_hook(_m, _inp, output):
        is_tuple = isinstance(output, tuple)
        hidden = output[0] if is_tuple else output
        idx = encoded["attention_mask"].sum(dim=1).long() - 1
        new_hidden = hidden.clone()
        new_hidden[torch.arange(hidden.shape[0], device=hidden.device), idx] = target_last_token_value.to(hidden.dtype)
        captured["overwritten_residual"] = new_hidden.detach()
        if is_tuple:
            return (new_hidden,) + output[1:]
        return new_hidden

    handle = layer.register_forward_hook(overwrite_hook)
    try:
        with torch.no_grad():
            outputs = model(**encoded, use_cache=False)
    finally:
        handle.remove()
    logits = get_last_token(outputs.logits, encoded["attention_mask"])[0]
    normed = get_last_token(model.model.norm(captured["overwritten_residual"]), encoded["attention_mask"])[0]
    return {"logits": logits, "normed": normed}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="Qwen/Qwen2.5-1.5B-Instruct")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--layer", type=int, default=27)
    parser.add_argument("--n-examples", type=int, default=8)
    parser.add_argument("--raw-layers", default="artifacts/safe_mech/raw_layer_examples.pt")
    parser.add_argument("--out-dir", default="artifacts/safe_mech")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_layers = torch.load(args.raw_layers)
    direction = extract_contrasts(cell_means_from_examples(raw_layers["fit"][args.layer]))["p_contrast"]

    rows = build_safe_mech_assay(16)
    validate_safe_mech_assay(rows)
    abstain_rows = [r for r in rows if r["split"] == "carrier-test" and r["policy"] == "abstain"][: args.n_examples]

    tokenizer, model = load_model(args.model, args.device, "float32")
    device = args.device

    unit = direction / direction.norm()
    results = []
    for row in abstain_rows:
        baseline, encoded = capture_forward(model, tokenizer, device, row["prompt"], args.layer)
        delta = -torch.dot(baseline["mlp_output"], unit.to(device)) * unit.to(device)
        target_last_token = baseline["block_residual"] + delta

        b_mlp_hook = forward_with_mlp_removal(model, tokenizer, device, row["prompt"], args.layer, direction)
        c_overwrite = forward_with_residual_overwrite(model, tokenizer, device, row["prompt"], args.layer, target_last_token)

        residual_diff = float((b_mlp_hook["block_residual"] - target_last_token).norm())
        normed_diff = float((b_mlp_hook["normed"] - c_overwrite["normed"]).norm())
        logits_diff = float((b_mlp_hook["logits"] - c_overwrite["logits"]).abs().max())
        topk_b = torch.topk(b_mlp_hook["logits"], 5).indices.tolist()
        topk_c = torch.topk(c_overwrite["logits"], 5).indices.tolist()
        results.append({
            "example_id": row["example_id"],
            "residual_diff_norm": residual_diff,
            "normed_state_diff_norm": normed_diff,
            "logits_max_abs_diff": logits_diff,
            "top5_token_ids_mlp_hook": topk_b,
            "top5_token_ids_residual_overwrite": topk_c,
            "top1_agrees": topk_b[0] == topk_c[0],
            "argmax_mlp_hook": int(torch.argmax(b_mlp_hook["logits"])),
            "argmax_residual_overwrite": int(torch.argmax(c_overwrite["logits"])),
        })

    n_agree = sum(1 for r in results if r["top1_agrees"])
    max_logits_diff = max(r["logits_max_abs_diff"] for r in results)
    verdict = "STATE_EQUIVALENCE_CONFIRMED" if max_logits_diff < 1e-2 and n_agree == len(results) else "IMPLEMENTATION_INCONSISTENCY"

    summary = {"role": "SAFE_MECH_BENIGN_PROXY", "layer": args.layer, "n_examples": len(results), "n_top1_agree": n_agree, "max_logits_diff": max_logits_diff, "verdict": verdict, "per_example": results}
    Path(out_dir / "exact_state_equivalence.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps({k: v for k, v in summary.items() if k != "per_example"}, indent=2))


if __name__ == "__main__":
    main()
