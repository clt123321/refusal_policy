#!/usr/bin/env python3
"""Reload and validate one V6 repair adapter; no paths are implicit."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def validate_reload(base: Path, adapter: Path, device: str, dtype: str) -> dict:
    try:
        import torch
        from peft import PeftModel
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as exc:
        raise RuntimeError("REPAIR_RUNTIME_DEPENDENCY_MISSING: torch/transformers/peft") from exc
    if not (base / "config.json").is_file():
        raise ValueError(f"BASE_MODEL_NOT_FOUND: {base}")
    if not (adapter / "adapter_config.json").is_file():
        raise ValueError(f"ADAPTER_NOT_FOUND: {adapter}")
    selected_dtype = torch.float16 if dtype == "float16" else torch.float32
    tokenizer = AutoTokenizer.from_pretrained(base.as_posix())
    model = AutoModelForCausalLM.from_pretrained(
        base.as_posix(), torch_dtype=selected_dtype,
    ).to(device).eval()
    loaded = PeftModel.from_pretrained(model, adapter.as_posix()).eval()
    finite = all(bool(torch.isfinite(parameter).all()) for parameter in loaded.parameters())
    return {
        "reload_pass": finite, "finite": finite, "base": str(base),
        "adapter": str(adapter), "device": device, "dtype": dtype,
        "tokenizer_class": tokenizer.__class__.__name__,
        "adapter_files": sorted(path.name for path in adapter.iterdir()),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Reload a V6 repair adapter")
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--adapter", type=Path, required=True)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--dtype", choices=("float16", "float32"), default="float16")
    parser.add_argument("--receipt", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = validate_reload(args.base, args.adapter, args.device, args.dtype)
    encoded = json.dumps(result, sort_keys=True, indent=2)
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(encoded)
    print(encoded)
    return 0 if result["reload_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
