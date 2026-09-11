import argparse
import json
from pathlib import Path

from src.data.proxy import build_proxy_assay, validate_assay


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples-per-cell", type=int, default=8)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rows = build_proxy_assay(args.samples_per_cell)
    validate_assay(rows)
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n")


if __name__ == "__main__":
    main()
