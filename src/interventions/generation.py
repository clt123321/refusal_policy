from contextlib import ExitStack, contextmanager
from typing import Any

import torch

from src.models.runtime import layer_modules


@contextmanager
def steer_module(module: Any, mode: str, direction: torch.Tensor, alpha: float = 1.0, first_token_only: bool = False, token_scope: str | None = None):
    if mode not in ("remove", "add", "patch"):
        raise ValueError(f"unknown mode {mode}")
    unit = direction / direction.norm()
    scope = token_scope or ("prompt_first" if first_token_only else "all")
    if scope not in ("all", "prompt_all", "prompt_first", "prompt_last", "gen_first", "gen_all"):
        raise ValueError(f"unknown token_scope {scope}")
    state = {"seen_decode_call": False}

    def hook(_module: Any, _inputs: tuple[Any, ...], output: Any):
        is_tuple = isinstance(output, tuple)
        hidden = output[0] if is_tuple else output
        target_direction = unit.to(hidden.dtype).to(hidden.device)
        seq_len = hidden.shape[1]
        is_prompt_call = seq_len > 1
        mask = torch.zeros(seq_len, dtype=hidden.dtype, device=hidden.device)
        if scope == "all":
            mask[:] = 1.0
        elif scope == "prompt_all" and is_prompt_call:
            mask[:] = 1.0
        elif scope == "prompt_first" and is_prompt_call:
            mask[0] = 1.0
        elif scope == "prompt_last" and is_prompt_call:
            mask[-1] = 1.0
        elif scope == "gen_all" and not is_prompt_call:
            mask[:] = 1.0
        elif scope == "gen_first" and not is_prompt_call and not state["seen_decode_call"]:
            mask[:] = 1.0
        if not is_prompt_call:
            state["seen_decode_call"] = True
        if mode == "remove":
            projection = torch.einsum("bsd,d->bs", hidden, target_direction)
            delta = -torch.einsum("bs,d->bsd", projection * mask, target_direction)
        else:
            delta = alpha * mask.view(1, -1, 1) * target_direction.view(1, 1, -1)
        new_hidden = hidden + delta
        if is_tuple:
            return (new_hidden,) + output[1:]
        return new_hidden

    handle = module.register_forward_hook(hook)
    try:
        yield
    finally:
        handle.remove()


@contextmanager
def steer_layer(model: Any, layer_index: int, mode: str, direction: torch.Tensor, alpha: float = 1.0, first_token_only: bool = False, token_scope: str | None = None):
    layer = layer_modules(model)[layer_index]
    with steer_module(layer, mode, direction, alpha=alpha, first_token_only=first_token_only, token_scope=token_scope):
        yield


@contextmanager
def steer_writer(model: Any, layer_index: int, writer: str, mode: str, direction: torch.Tensor, alpha: float = 1.0, first_token_only: bool = False):
    if writer not in ("attn_output", "mlp_output"):
        raise ValueError(f"unknown writer {writer}")
    layer = layer_modules(model)[layer_index]
    module = layer.self_attn if writer == "attn_output" else layer.mlp
    with steer_module(module, mode, direction, alpha=alpha, first_token_only=first_token_only):
        yield


@contextmanager
def steer_remove_then_patch(model: Any, remove_layer: int, remove_direction: torch.Tensor, patch_layer: int, patch_direction: torch.Tensor, patch_alpha: float):
    with steer_layer(model, remove_layer, "remove", remove_direction):
        with steer_layer(model, patch_layer, "patch", patch_direction, alpha=patch_alpha):
            yield


@contextmanager
def steer_multi_layer(model: Any, mode: str, layer_directions: dict[int, torch.Tensor], alphas: dict[int, float] | None = None, first_token_only: bool = False, token_scope: str | None = None):
    alphas = alphas or {}
    with ExitStack() as stack:
        for layer_index, direction in layer_directions.items():
            stack.enter_context(steer_layer(model, layer_index, mode, direction, alpha=alphas.get(layer_index, 1.0), first_token_only=first_token_only, token_scope=token_scope))
        yield


@contextmanager
def steer_multi_remove_then_patch(model: Any, remove_layer_directions: dict[int, torch.Tensor], patch_layer: int, patch_direction: torch.Tensor, patch_alpha: float):
    with steer_multi_layer(model, "remove", remove_layer_directions):
        with steer_layer(model, patch_layer, "patch", patch_direction, alpha=patch_alpha):
            yield


@contextmanager
def steer_subspace_multi_layer(model: Any, layer_directions: dict[int, torch.Tensor]):
    """Remove a k-dim orthonormal subspace per layer by stacking one remove-hook per basis vector."""
    with ExitStack() as stack:
        for layer_index, directions in layer_directions.items():
            for direction in directions:
                stack.enter_context(steer_layer(model, layer_index, "remove", direction))
        yield
