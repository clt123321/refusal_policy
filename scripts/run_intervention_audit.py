import argparse
import json
from pathlib import Path

import torch

from src.data.safe_mech import build_safe_mech_assay, validate_safe_mech_assay
from src.models.runtime import encode, final_nonpad, layer_modules, load_model
from src.stats.contrasts import cell_means_from_examples, extract_contrasts


def capture_with_inline_removal(model, tokenizer, device, rows, num_layers, removal_directions):
    layers = layer_modules(model)
    removal_directions = removal_directions or {}
    captured = {}

    def make_hook(i):
        unit = None
        if i in removal_directions:
            d = removal_directions[i]
            unit = d / d.norm()

        def hook(_m, _inp, output):
            is_tuple = isinstance(output, tuple)
            hidden = output[0] if is_tuple else output
            if unit is not None:
                target = unit.to(hidden.dtype).to(hidden.device)
                projection = torch.einsum("bsd,d->bs", hidden, target)
                hidden = hidden - torch.einsum("bs,d->bsd", projection, target)
            captured[i] = hidden.detach()
            if unit is not None:
                return (hidden,) + output[1:] if is_tuple else hidden
            return None

        return hook

    handles = [layers[i].register_forward_hook(make_hook(i)) for i in range(num_layers)]
    per_layer_vectors = {i: [] for i in range(num_layers)}
    try:
        for row in rows:
            encoded = encode(tokenizer, [row["prompt"]], device)
            with torch.inference_mode():
                model(**encoded, use_cache=False)
            for i in range(num_layers):
                state = final_nonpad(captured[i], encoded["attention_mask"])[0].float().cpu()
                per_layer_vectors[i].append(state)
    finally:
        for h in handles:
            h.remove()
    return per_layer_vectors


def projection_stats(vectors, direction):
    unit = direction / direction.norm()
    projections = torch.stack([torch.dot(v, unit) for v in vectors])
    return {"mean_abs_projection": float(projections.abs().mean()), "mean_projection": float(projections.mean())}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="Qwen/Qwen2.5-1.5B-Instruct")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--dtype", default="float16")
    parser.add_argument("--n-per-split", type=int, default=16)
    parser.add_argument("--num-layers", type=int, default=28)
    parser.add_argument("--raw-layers", default="artifacts/safe_mech/raw_layer_examples.pt")
    parser.add_argument("--out-dir", default="artifacts/safe_mech")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_layers = torch.load(args.raw_layers)
    all_layer_directions = {layer: extract_contrasts(cell_means_from_examples(raw_layers["fit"][layer]))["p_contrast"] for layer in range(args.num_layers)}

    rows = build_safe_mech_assay(args.n_per_split)
    validate_safe_mech_assay(rows)
    test_rows = [r for r in rows if r["split"] == "carrier-test"]
    abstain_rows = [r for r in test_rows if r["policy"] == "abstain"]

    tokenizer, model = load_model(args.model, args.device, args.dtype)
    device = args.device

    scopes = {
        "baseline": {},
        "remove_L18": {18: all_layer_directions[18]},
        "remove_L18_23": {l: all_layer_directions[l] for l in range(18, 24)},
        "remove_all_0_27": all_layer_directions,
    }

    results = {}
    for scope_name, removal in scopes.items():
        per_layer_vectors = capture_with_inline_removal(model, tokenizer, device, abstain_rows, args.num_layers, removal)
        results[scope_name] = {layer: projection_stats(vectors, all_layer_directions[layer]) for layer, vectors in per_layer_vectors.items()}

    csv_lines = ["scope,layer,mean_abs_projection,mean_projection,is_ablated_here"]
    for scope_name, per_layer in results.items():
        ablated_here = set(scopes[scope_name].keys())
        for layer, stats in per_layer.items():
            csv_lines.append(f"{scope_name},{layer},{stats['mean_abs_projection']},{stats['mean_projection']},{layer in ablated_here}")
    Path(out_dir / "intervention_audit_layerwise_projection.csv").write_text("\n".join(csv_lines) + "\n")
    Path(out_dir / "intervention_audit_layerwise_projection.json").write_text(json.dumps(results, indent=2))
    print("done")


if __name__ == "__main__":
    main()
