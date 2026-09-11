from collections.abc import Iterable
from contextlib import contextmanager
from typing import Any

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def load_model(model_id: str, device: str = "cuda", dtype: str = "float16"):
    torch_dtype = getattr(torch, dtype) if dtype != "auto" else "auto"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch_dtype)
    model.eval().to(device)
    return tokenizer, model


def layer_modules(model: Any) -> list[Any]:
    if hasattr(model, "transformer") and hasattr(model.transformer, "h"):
        return list(model.transformer.h)
    if hasattr(model, "model") and hasattr(model.model, "layers"):
        return list(model.model.layers)
    raise ValueError("unsupported transformer layer layout")


def _hidden(output: Any) -> torch.Tensor:
    return output[0] if isinstance(output, tuple) else output


@contextmanager
def capture_layer(model: Any, layer_index: int):
    captured: dict[str, torch.Tensor] = {}
    def hook(_module: Any, _inputs: tuple[Any, ...], output: Any):
        hidden = _hidden(output)
        if hidden.ndim != 3:
            raise ValueError(f"expected [batch, sequence, hidden], got {tuple(hidden.shape)}")
        captured["output"] = hidden.detach()
    handle = layer_modules(model)[layer_index].register_forward_hook(hook)
    try:
        yield captured
    finally:
        handle.remove()


def final_nonpad(hidden: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
    indices = attention_mask.sum(dim=1).to(torch.long) - 1
    return hidden[torch.arange(hidden.shape[0], device=hidden.device), indices]


def encode(tokenizer: Any, texts: Iterable[str], device: str):
    batch = tokenizer(list(texts), return_tensors="pt", padding=True, truncation=True)
    return {key: value.to(device) for key, value in batch.items()}
