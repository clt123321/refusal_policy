import argparse
import json
from pathlib import Path

import torch

from src.data.safe_mech import build_safe_mech_assay, validate_safe_mech_assay
from src.interventions.generation import steer_multi_layer
from src.models.runtime import encode, final_nonpad, layer_modules, load_model
from src.stats.contrasts import cell_means_from_examples, extract_contrasts


def capture_sentinel(model, tokenizer, device, rows, sentinel_layer, ctx_factory=None):
    layer = layer_modules(model)[sentinel_layer]
    captured = {}

    def hook(_module, _inputs, output):
        hidden = output[0] if isinstance(output, tuple) else output
        captured["hidden"] = hidden.detach()

    handle = layer.register_forward_hook(hook)
    vectors = []
    try:
        for row in rows:
            encoded = encode(tokenizer, [row["prompt"]], device)
            if ctx_factory is None:
                with torch.inference_mode():
                    model(**encoded, use_cache=False)
            else:
                with ctx_factory():
                    with torch.inference_mode():
                        model(**encoded, use_cache=False)
            state = final_nonpad(captured["hidden"], encoded["attention_mask"])[0].float().cpu()
            vectors.append(state)
    finally:
        handle.remove()
    return vectors


def separation_effect_size(direction, vectors_a, vectors_b):
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
    parser.add_argument("--ablation-start", type=int, default=18)
    parser.add_argument("--ablation-end", type=int, default=23)
    parser.add_argument("--sentinel-layer", type=int, default=27)
    parser.add_argument("--raw-layers", default="artifacts/safe_mech/raw_layer_examples.pt")
    parser.add_argument("--out-dir", default="artifacts/safe_mech")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_layers = torch.load(args.raw_layers)
    ablation_layers = list(range(args.ablation_start, args.ablation_end + 1))
    upstream_directions = {layer: extract_contrasts(cell_means_from_examples(raw_layers["fit"][layer]))["p_contrast"] for layer in ablation_layers}
    sentinel_direction = extract_contrasts(cell_means_from_examples(raw_layers["fit"][args.sentinel_layer]))["p_contrast"]

    rows = build_safe_mech_assay(args.n_per_split)
    validate_safe_mech_assay(rows)
    test_rows = [r for r in rows if r["split"] == "carrier-test"]
    abstain_rows = [r for r in test_rows if r["policy"] == "abstain"]
    answer_rows = [r for r in test_rows if r["policy"] == "answer"]

    tokenizer, model = load_model(args.model, args.device, args.dtype)
    device = args.device

    def remove_ctx():
        return steer_multi_layer(model, "remove", upstream_directions)

    baseline_abstain_vecs = capture_sentinel(model, tokenizer, device, abstain_rows, args.sentinel_layer, None)
    baseline_answer_vecs = capture_sentinel(model, tokenizer, device, answer_rows, args.sentinel_layer, None)
    ablated_abstain_vecs = capture_sentinel(model, tokenizer, device, abstain_rows, args.sentinel_layer, remove_ctx)
    ablated_answer_vecs = capture_sentinel(model, tokenizer, device, answer_rows, args.sentinel_layer, remove_ctx)

    baseline_separation = separation_effect_size(sentinel_direction, baseline_abstain_vecs, baseline_answer_vecs)
    ablated_separation = separation_effect_size(sentinel_direction, ablated_abstain_vecs, ablated_answer_vecs)

    summary = {
        "role": "SAFE_MECH_BENIGN_PROXY",
        "ablation_layers": ablation_layers,
        "sentinel_layer": args.sentinel_layer,
        "baseline_sentinel_separation_effect_size": baseline_separation,
        "upstream_ablated_sentinel_separation_effect_size": ablated_separation,
        "retention_fraction": ablated_separation / baseline_separation if abs(baseline_separation) > 1e-9 else float("nan"),
        "interpretation": "If retention_fraction is close to 1, the late-layer P-signal survives upstream ablation (consistent with redundant/shared downstream encoding). If close to 0, upstream ablation removes the signal at the sentinel too.",
    }
    Path(out_dir / "c05_shared_gate_sentinel.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
