import argparse
import json
from pathlib import Path

import torch

from src.data.proxy import validate_assay
from src.hooks.capture import collect_layer_means
from src.models.runtime import load_model
from src.stats.contrasts import extract_contrasts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="sshleifer/tiny-gpt2")
    parser.add_argument("--data", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--dtype", default="float32")
    args = parser.parse_args()
    rows = [json.loads(line) for line in Path(args.data).read_text().splitlines()]
    validate_assay(rows)
    tokenizer, model = load_model(args.model, args.device, args.dtype)
    means = collect_layer_means(model, tokenizer, rows, [0], args.device)
    contrasts = {str(layer): {key: value.tolist() for key, value in extract_contrasts(cells).items()} for layer, cells in means.items()}
    payload = {"role": "PIPELINE_VALIDATION_ONLY", "model": args.model, "contrasts": contrasts}
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
