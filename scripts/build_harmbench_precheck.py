from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validation", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--per-class", type=int, default=16)
    args = parser.parse_args()
    data = json.loads(args.validation.read_text())
    metadata = {row["BehaviorID"]: row for row in csv.DictReader(args.metadata.open())}
    candidates = []
    for behavior_id, items in data.items():
        meta = metadata.get(behavior_id)
        if not meta or meta.get("FunctionalCategory") != "standard" or meta.get("ContextString", ""):
            continue
        by_label = {0: [], 1: []}
        for index, item in enumerate(items):
            votes = [item.get(key) for key in ("human_0", "human_1", "human_2")]
            if not all(v in (0, 1) for v in votes):
                continue
            label = 1 if sum(votes) >= 2 else 0
            generation = item.get("generation")
            if not isinstance(generation, str) or not generation.strip():
                continue
            sample_id = hashlib.sha256(f"{behavior_id}\0{index}\0{item.get('test_case', '')}".encode()).hexdigest()[:32]
            by_label[label].append({
                "sample_id": f"hb-val-{sample_id}",
                "behavior_id": behavior_id,
                "behavior": meta["Behavior"],
                "context": "",
                "generation": generation,
                "human_votes": votes,
                "human_majority": label,
                "source_item_index": index,
            })
        for label, items_for_label in by_label.items():
            if items_for_label:
                keyed = []
                for item in items_for_label:
                    digest = hashlib.sha256(f"{args.seed}\0{item['sample_id']}".encode()).hexdigest()
                    keyed.append((digest, item))
                keyed.sort(key=lambda pair: pair[0])
                candidates.append((label, keyed[0][0], keyed[0][1]))
    selected = []
    for label in (0, 1):
        pool = sorted((item for item_label, _, item in candidates if item_label == label), key=lambda item: hashlib.sha256(f"{args.seed}\0{item['sample_id']}".encode()).hexdigest())
        selected.extend(pool[: args.per_class])
    if len([x for x in selected if x["human_majority"] == 0]) != args.per_class or len([x for x in selected if x["human_majority"] == 1]) != args.per_class:
        raise RuntimeError("INSUFFICIENT_BALANCED_HUMAN_LABELED_SAMPLES")
    selected.sort(key=lambda item: item["sample_id"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({
        "status": "DEV_PRECHECK_FIXED",
        "seed": args.seed,
        "selection_rule": "standard non-contextual only; human_0/1/2 majority; at most one sample per behavior and class; stable hash order",
        "source_validation_sha256": sha256(args.validation),
        "source_metadata_sha256": sha256(args.metadata),
        "sample_count": len(selected),
        "positive_count": sum(x["human_majority"] for x in selected),
        "negative_count": sum(1 - x["human_majority"] for x in selected),
        "samples": selected,
    }, ensure_ascii=False, indent=2))
    print(json.dumps({
        "output": str(args.output.resolve()),
        "sample_count": len(selected),
        "positive_count": sum(x["human_majority"] for x in selected),
        "negative_count": sum(1 - x["human_majority"] for x in selected),
        "sample_ids": [x["sample_id"] for x in selected],
        "file_sha256": sha256(args.output),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
