from collections import defaultdict
from typing import Any

import torch

from src.models.runtime import capture_layer, encode, final_nonpad


def collect_layer_means(model: Any, tokenizer: Any, rows: list[dict[str, Any]], layers: list[int], device: str, batch_size: int = 8) -> dict[int, dict[str, torch.Tensor]]:
    grouped: dict[int, dict[str, list[torch.Tensor]]] = defaultdict(lambda: defaultdict(list))
    for start in range(0, len(rows), batch_size):
        batch_rows = rows[start:start + batch_size]
        encoded = encode(tokenizer, [row["text"] for row in batch_rows], device)
        for layer in layers:
            with capture_layer(model, layer) as captured:
                model(**encoded, use_cache=False)
            states = final_nonpad(captured["output"], encoded["attention_mask"]).float().cpu()
            for state, row in zip(states, batch_rows):
                grouped[layer][f"h{row['h']}_p{row['p']}"].append(state)
    return {layer: {cell: torch.stack(values).mean(dim=0) for cell, values in cells.items()} for layer, cells in grouped.items()}
