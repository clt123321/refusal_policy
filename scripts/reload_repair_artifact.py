#!/usr/bin/env python3
"""Reload and validate one V6 repair adapter; no paths are implicit."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def validate_reload(base: Path, adapter: Path, device: str, dtype: str, reference: Path | None = None) -> dict:
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
    result = {
        "reload_pass": finite, "finite": finite, "base": str(base),
        "adapter": str(adapter), "device": device, "dtype": dtype,
        "tokenizer_class": tokenizer.__class__.__name__,
        "adapter_files": sorted(path.name for path in adapter.iterdir()),
    }
    if reference:
        if not reference.is_file():
            raise ValueError(f"MEMORY_REFERENCE_NOT_FOUND: {reference}")
        prompt = "Answer with the word SAFE in uppercase."
        rendered = tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True,
        )
        inputs = tokenizer(rendered, return_tensors="pt").to(device)
        with torch.inference_mode():
            logits = loaded(**inputs, use_cache=False).logits[:, -1, :].detach().float().cpu()
            output = loaded.generate(**inputs, max_new_tokens=8, do_sample=False, pad_token_id=tokenizer.eos_token_id)
        generated = tokenizer.decode(output[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True)
        expected = torch.load(reference, map_location="cpu", weights_only=True).float()
        max_diff = float((logits - expected).abs().max())
        result["memory_reload_comparison"] = {
            "reference": str(reference), "prompt": prompt, "memory_output": None,
            "reloaded_output": generated, "logits_max_abs_diff": max_diff,
            "logits_tolerance": 1e-5, "within_tolerance": max_diff <= 1e-5,
        }
        result["reload_pass"] = bool(result["reload_pass"] and max_diff <= 1e-5)
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Reload a V6 repair adapter")
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--adapter", type=Path, required=True)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--dtype", choices=("float16", "float32"), default="float16")
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--reference", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = validate_reload(args.base, args.adapter, args.device, args.dtype, args.reference)
    encoded = json.dumps(result, sort_keys=True, indent=2)
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(encoded)
    print(encoded)
    return 0 if result["reload_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
