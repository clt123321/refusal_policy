import argparse
import itertools
import json
from pathlib import Path

import torch

from src.data.safe_mech import build_safe_mech_assay
from src.models.runtime import encode, layer_modules, load_model


def writer_module(model, layer, writer):
    layer_mod = layer_modules(model)[layer]
    return layer_mod.self_attn if writer == "attn_output" else layer_mod.mlp


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="Qwen/Qwen2.5-1.5B-Instruct")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--n-examples", type=int, default=4)
    parser.add_argument("--raw-layers", default="artifacts/safe_mech/raw_layer_examples.pt")
    parser.add_argument("--out-dir", default="artifacts/safe_mech")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_layers = torch.load(args.raw_layers)

    writers = [(20, "attn_output"), (24, "attn_output"), (27, "mlp_output"), (26, "mlp_output")]
    from src.stats.contrasts import cell_means_from_examples, extract_contrasts
    directions = {layer: extract_contrasts(cell_means_from_examples(raw_layers["fit"][layer]))["p_contrast"] for layer, _ in writers}

    shared_blocks = [(10, "mlp.down_proj"), (15, "self_attn.o_proj"), (5, "mlp.down_proj")]

    tokenizer, model = load_model(args.model, args.device, "float32")
    device = args.device

    rows = build_safe_mech_assay(16)
    abstain_examples = [r for r in rows if r["split"] == "construct-fit" and r["policy"] == "abstain"][: args.n_examples]

    def get_param(layer, suffix):
        layer_mod = layer_modules(model)[layer]
        obj = layer_mod
        for part in suffix.split("."):
            obj = getattr(obj, part)
        return obj.weight

    gradients = {(w, b): [] for w in writers for b in shared_blocks}

    for row in abstain_examples:
        encoded = encode(tokenizer, [row["prompt"]], device)
        captured = {}

        def make_hook(key):
            def hook(_m, _inp, output):
                hidden = output[0] if isinstance(output, tuple) else output
                captured[key] = hidden
            return hook

        handles = [writer_module(model, layer, writer).register_forward_hook(make_hook((layer, writer))) for layer, writer in writers]
        try:
            model.zero_grad(set_to_none=True)
            output = model(**encoded, use_cache=False)
            for (layer, writer) in writers:
                hidden = captured[(layer, writer)]
                unit = directions[layer] / directions[layer].norm()
                coordinate = torch.einsum("bsd,d->", hidden[:, -1:, :], unit.to(hidden.dtype).to(hidden.device))
                params = [get_param(b_layer, b_suffix) for b_layer, b_suffix in shared_blocks]
                grads = torch.autograd.grad(coordinate, params, retain_graph=True, allow_unused=True)
                for block, grad in zip(shared_blocks, grads):
                    if grad is not None:
                        gradients[((layer, writer), block)].append(grad.detach().flatten().float().cpu())
        finally:
            for h in handles:
                h.remove()

    avg_gradients = {}
    for key, grad_list in gradients.items():
        if grad_list:
            avg_gradients[key] = torch.stack(grad_list).mean(dim=0)

    rows_out = []
    for block in shared_blocks:
        writer_keys = [w for w in writers if (w, block) in avg_gradients]
        for w1, w2 in itertools.combinations(writer_keys, 2):
            g1 = avg_gradients[(w1, block)]
            g2 = avg_gradients[(w2, block)]
            cos = float(torch.nn.functional.cosine_similarity(g1, g2, dim=0))
            rows_out.append({"block": f"L{block[0]}_{block[1]}", "writer_a": f"L{w1[0]}_{w1[1]}", "writer_b": f"L{w2[0]}_{w2[1]}", "cosine": cos})

    Path(out_dir / "writer_parameter_sensitivity.csv").write_text(
        "block,writer_a,writer_b,cosine\n" + "\n".join(f"{r['block']},{r['writer_a']},{r['writer_b']},{r['cosine']}" for r in rows_out) + "\n"
    )
    Path(out_dir / "writer_parameter_sensitivity.json").write_text(json.dumps(rows_out, indent=2))
    print(json.dumps(rows_out, indent=2))


if __name__ == "__main__":
    main()
