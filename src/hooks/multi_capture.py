from contextlib import ExitStack, contextmanager
from typing import Any

import torch

from src.models.runtime import encode, final_nonpad, layer_modules


@contextmanager
def capture_all_layers(model: Any):
    layers = layer_modules(model)
    captured: dict[int, torch.Tensor] = {}

    def make_hook(index: int):
        def hook(_module: Any, _inputs: tuple[Any, ...], output: Any):
            hidden = output[0] if isinstance(output, tuple) else output
            captured[index] = hidden.detach()
        return hook

    with ExitStack() as stack:
        for i, layer in enumerate(layers):
            stack.enter_context(_handle_ctx(layer.register_forward_hook(make_hook(i))))
        yield captured


@contextmanager
def capture_writer_outputs(model: Any, layer_indices: list[int]):
    layers = layer_modules(model)
    captured: dict[tuple[int, str], torch.Tensor] = {}

    def make_hook(index: int, module_name: str):
        def hook(_module: Any, _inputs: tuple[Any, ...], output: Any):
            hidden = output[0] if isinstance(output, tuple) else output
            captured[(index, module_name)] = hidden.detach()
        return hook

    with ExitStack() as stack:
        for i in layer_indices:
            stack.enter_context(_handle_ctx(layers[i].self_attn.register_forward_hook(make_hook(i, "attn_output"))))
            stack.enter_context(_handle_ctx(layers[i].mlp.register_forward_hook(make_hook(i, "mlp_output"))))
        yield captured


@contextmanager
def _handle_ctx(handle: Any):
    try:
        yield handle
    finally:
        handle.remove()


def collect_all_layer_means(model: Any, tokenizer: Any, rows: list[dict[str, Any]], device: str, batch_size: int = 8) -> dict[int, dict[str, list[torch.Tensor]]]:
    grouped: dict[int, dict[str, list[torch.Tensor]]] = {}
    for start in range(0, len(rows), batch_size):
        batch_rows = rows[start:start + batch_size]
        encoded = encode(tokenizer, [row["prompt"] for row in batch_rows], device)
        with capture_all_layers(model) as captured:
            model(**encoded, use_cache=False)
        for layer_index, hidden in captured.items():
            states = final_nonpad(hidden, encoded["attention_mask"]).float().cpu()
            layer_bucket = grouped.setdefault(layer_index, {})
            for state, row in zip(states, batch_rows):
                key = f"h{row['h']}_p{row['p']}"
                layer_bucket.setdefault(key, []).append(state)
    return grouped


def collect_writer_means(model: Any, tokenizer: Any, rows: list[dict[str, Any]], layer_indices: list[int], device: str, batch_size: int = 8) -> dict[tuple[int, str], dict[str, list[torch.Tensor]]]:
    grouped: dict[tuple[int, str], dict[str, list[torch.Tensor]]] = {}
    for start in range(0, len(rows), batch_size):
        batch_rows = rows[start:start + batch_size]
        encoded = encode(tokenizer, [row["prompt"] for row in batch_rows], device)
        with capture_writer_outputs(model, layer_indices) as captured:
            model(**encoded, use_cache=False)
        for key, hidden in captured.items():
            states = final_nonpad(hidden, encoded["attention_mask"]).float().cpu()
            bucket = grouped.setdefault(key, {})
            for state, row in zip(states, batch_rows):
                cell = f"h{row['h']}_p{row['p']}"
                bucket.setdefault(cell, []).append(state)
    return grouped
