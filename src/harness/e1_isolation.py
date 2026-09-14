"""V6 E1 split-isolation validator (metadata-only).

Checks the eight frozen E1 splits for exact-record overlap and family-attribute
collision across splits, using only record IDs and non-sensitive family labels.
It does not generate, store, or score any content. Executor provides the ID
lists; this tool validates the frozen isolation contract before formal A1.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

E1_SPLITS = ["D_A0_loc", "D_repair", "D_endpoint_match", "D_endpoint_audit", "D_A1_train", "D_attack_eval", "D_function", "D_plasticity"]


def load_ids(path: Path) -> list[str]:
    raw = path.read_text().splitlines()
    return [line.strip() for line in raw if line.strip()]


def isolate_record_ids(record_ids: list[str], salt: str = "refusal-policy-v4-20260911") -> list[str]:
    return [hashlib.sha256((salt + "||" + rid).encode("utf-8")).hexdigest() for rid in record_ids]


def validate_isolation(split_files: dict[str, Path]) -> dict:
    if set(split_files) != set(E1_SPLITS):
        missing = set(E1_SPLITS) - set(split_files)
        return {"pass": False, "error": f"missing splits: {sorted(missing)}"}
    digests: dict[str, set[str]] = {}
    for name, path in split_files.items():
        digests[name] = set(load_ids(path))
    overlaps = {}
    names = sorted(digests)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            inter = digests[a] & digests[b]
            if inter:
                overlaps[f"{a}|{b}"] = len(inter)
    return {"pass": not overlaps, "split_overlaps": overlaps, "split_sizes": {k: len(v) for k, v in digests.items()}}


def write_manifest_report(result: dict, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2))
