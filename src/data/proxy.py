from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class ProxyExample:
    example_id: str
    family: str
    topic: str
    action: str
    text: str
    h: int
    p: int


def build_proxy_assay(samples_per_cell: int = 8) -> list[dict[str, Any]]:
    rows = []
    for h, topic in enumerate(("alpha", "beta")):
        for p, action in enumerate(("answer", "abstain")):
            for i in range(samples_per_cell):
                rows.append({"example_id": f"proxy-{h}-{p}-{i}", "family": f"family-{i % 4}", "topic": topic, "action": action, "text": f"Topic {topic}: explain {topic}. Requested action: {action}.", "h": h, "p": p, "split": "proxy-dev", "role": "PIPELINE_VALIDATION_ONLY"})
    return rows


def validate_assay(rows: list[dict[str, Any]]) -> None:
    cells = {(row["h"], row["p"]) for row in rows}
    if cells != {(0, 0), (0, 1), (1, 0), (1, 1)}:
        raise ValueError(f"expected four HxP cells, got {cells}")
    if any(row.get("role") != "PIPELINE_VALIDATION_ONLY" for row in rows):
        raise ValueError("proxy rows must be marked PIPELINE_VALIDATION_ONLY")
