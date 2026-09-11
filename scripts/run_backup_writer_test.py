import argparse
import json
from pathlib import Path

import torch

from src.data.safe_mech import build_safe_mech_assay, validate_safe_mech_assay
from src.hooks.multi_capture import capture_writer_outputs
from src.interventions.generation import steer_multi_layer
from src.models.runtime import encode, final_nonpad, load_model
from src.stats.contrasts import cell_means_from_examples, extract_contrasts


def capture_writers_under(model, tokenizer, device, rows, num_layers, ctx_factory=None):
    per_key_vectors = {}
    for row in rows:
        encoded = encode(tokenizer, [row["prompt"]], device)
        with capture_writer_outputs(model, list(range(num_layers))) as captured:
            if ctx_factory is None:
                with torch.inference_mode():
                    model(**encoded, use_cache=False)
            else:
                with ctx_factory():
                    with torch.inference_mode():
                        model(**encoded, use_cache=False)
        for key, hidden in captured.items():
            state = final_nonpad(hidden, encoded["attention_mask"])[0].float().cpu()
            per_key_vectors.setdefault(key, []).append((row, state))
    return per_key_vectors


def writer_scores_from_vectors(per_key_vectors, residual_directions):
    scores = {}
    for key, pairs in per_key_vectors.items():
        layer = key[0]
        unit = residual_directions[layer] / residual_directions[layer].norm()
        abstain = [torch.dot(v, unit) for row, v in pairs if row["p"] == 1]
        answer = [torch.dot(v, unit) for row, v in pairs if row["p"] == 0]
        if abstain and answer:
            scores[key] = float(torch.stack(abstain).mean() - torch.stack(answer).mean())
    return scores


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
    residual_directions = {layer: extract_contrasts(cell_means_from_examples(raw_layers["fit"][layer]))["p_contrast"] for layer in range(args.num_layers)}

    rows = build_safe_mech_assay(args.n_per_split)
    validate_safe_mech_assay(rows)
    test_rows = [r for r in rows if r["split"] == "carrier-test" and r["policy"] in ("answer", "abstain")]

    tokenizer, model = load_model(args.model, args.device, args.dtype)
    device = args.device

    def full_ablation_ctx():
        return steer_multi_layer(model, "remove", residual_directions)

    baseline_vectors = capture_writers_under(model, tokenizer, device, test_rows, args.num_layers, None)
    ablated_vectors = capture_writers_under(model, tokenizer, device, test_rows, args.num_layers, full_ablation_ctx)

    baseline_scores = writer_scores_from_vectors(baseline_vectors, residual_directions)
    ablated_scores = writer_scores_from_vectors(ablated_vectors, residual_directions)

    rows_out = []
    for key in baseline_scores:
        rows_out.append({
            "layer": key[0], "module": key[1],
            "baseline_score": baseline_scores[key],
            "ablated_score": ablated_scores.get(key, float("nan")),
            "delta": ablated_scores.get(key, float("nan")) - baseline_scores[key],
            "increased_magnitude": abs(ablated_scores.get(key, 0.0)) > abs(baseline_scores[key]),
        })
    rows_out.sort(key=lambda r: -abs(r["delta"]))

    Path(out_dir / "backup_writer_test.json").write_text(json.dumps(rows_out, indent=2))
    csv_lines = ["layer,module,baseline_score,ablated_score,delta,increased_magnitude"]
    for r in rows_out:
        csv_lines.append(f"{r['layer']},{r['module']},{r['baseline_score']},{r['ablated_score']},{r['delta']},{r['increased_magnitude']}")
    Path(out_dir / "backup_writer_test.csv").write_text("\n".join(csv_lines) + "\n")
    n_increased = sum(1 for r in rows_out if r["increased_magnitude"])
    print(f"{n_increased}/{len(rows_out)} writers show increased |score| after full ablation")
    print(json.dumps(rows_out[:8], indent=2))


if __name__ == "__main__":
    main()
