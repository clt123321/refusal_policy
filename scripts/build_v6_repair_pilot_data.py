from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).casefold()


def row_id(prompt: str, target: str, target_sha: str) -> str:
    payload = "\x00".join((normalize_text(prompt), target_sha, target)).encode()
    return f"pku-saferlhf-{sha256_bytes(payload)[:32]}"


def tokenized_example(tokenizer: Any, prompt: str, target: str) -> tuple[int, int]:
    rendered = tokenizer.apply_chat_template(
        [{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True
    )
    prompt_ids = tokenizer(rendered, add_special_tokens=False)["input_ids"]
    full_ids = tokenizer(rendered + target, add_special_tokens=False)["input_ids"]
    return len(full_ids), len(full_ids) - len(prompt_ids)


def choose_grouped(rows: list[dict[str, Any]], count: int, seed: int) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[row["prompt_norm"]].append(row)
    group_items = list(groups.values())
    random.Random(seed).shuffle(group_items)
    selected: list[dict[str, Any]] = []
    for group in group_items:
        if len(selected) + len(group) <= count:
            selected.extend(group)
        if len(selected) == count:
            break
    if len(selected) < count:
        raise RuntimeError(f"INSUFFICIENT_GROUP_ISOLATED_ROWS: requested={count}, selected={len(selected)}")
    return selected


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = b"".join((json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n").encode() for row in rows)
    path.write_bytes(encoded)
    return sha256_bytes(encoded)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--tokenizer", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--train-count", type=int, default=512)
    parser.add_argument("--validation-count", type=int, default=64)
    args = parser.parse_args()

    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer.as_posix())
    counts = Counter()
    candidates: list[dict[str, Any]] = []
    overlength: list[str] = []
    empty_target: list[str] = []
    invalid_tokens: list[str] = []
    source_sha = sha256_bytes(args.source.read_bytes())
    with args.source.open() as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                counts["blank_lines"] += 1
                continue
            counts["source_rows"] += 1
            row = json.loads(line)
            safe0 = row.get("is_response_0_safe") is True
            safe1 = row.get("is_response_1_safe") is True
            if safe0 == safe1:
                counts["excluded_safe_label_not_exactly_one"] += 1
                continue
            response_key = "response_0" if safe0 else "response_1"
            target = row.get(response_key)
            prompt = row.get("prompt")
            target_sha = row.get(f"{response_key}_sha256")
            if not isinstance(prompt, str) or not prompt.strip() or not isinstance(target, str) or not target.strip():
                counts["excluded_empty_prompt_or_target"] += 1
                if not isinstance(target, str) or not target.strip():
                    empty_target.append(str(line_number))
                continue
            full_tokens, target_tokens = tokenized_example(tokenizer, prompt, target)
            if target_tokens <= 0:
                counts["excluded_zero_target_tokens"] += 1
                invalid_tokens.append(str(line_number))
                continue
            if full_tokens > 1024:
                counts["excluded_overlength"] += 1
                overlength.append(str(line_number))
                continue
            item = {
                "id": row_id(prompt, target, str(target_sha or "")),
                "prompt": prompt,
                "target": target,
                "source_line": line_number,
                "source_target_field": response_key,
                "source_target_sha256": target_sha,
                "prompt_norm": normalize_text(prompt),
                "full_tokens": full_tokens,
                "target_tokens": target_tokens,
            }
            candidates.append(item)
            counts["eligible_before_dedup"] += 1

    by_id = {}
    for item in candidates:
        by_id[item["id"]] = item
    deduped = list(by_id.values())
    counts["excluded_duplicate_ids"] = len(candidates) - len(deduped)
    prompt_groups = Counter(item["prompt_norm"] for item in deduped)
    counts["exact_normalized_prompt_groups_gt1"] = sum(1 for value in prompt_groups.values() if value > 1)
    counts["exact_normalized_prompt_duplicate_rows"] = sum(value - 1 for value in prompt_groups.values() if value > 1)
    unique = [item for item in deduped if prompt_groups[item["prompt_norm"]] == 1]
    counts["eligible_group_isolated"] = len(unique)
    total_requested = args.train_count + args.validation_count
    if len(unique) < total_requested:
        raise RuntimeError(f"INSUFFICIENT_PILOT_ROWS: requested={total_requested}, available={len(unique)}")
    selected = choose_grouped(unique, total_requested, args.seed)
    train = selected[: args.train_count]
    validation = selected[args.train_count :]
    for item in train + validation:
        item.pop("prompt_norm", None)
    output_root = args.output_root
    train_sha = write_jsonl(output_root / "train.jsonl", train)
    validation_sha = write_jsonl(output_root / "validation.jsonl", validation)
    all_ids = [item["id"] for item in train + validation]
    train_ids = [item["id"] for item in train]
    validation_ids = [item["id"] for item in validation]
    manifest = {
        "dataset_id": "V6.E1.DEV.REPAIR_PILOT.PKU_SAFE_RLHF",
        "status": "DEV_ONLY_NOT_FORMAL",
        "source": {
            "repo_id": "PKU-Alignment/PKU-SafeRLHF",
            "repo_type": "dataset",
            "revision": "9421ffafec3fa40a1f1a7d567b4d525079477ecb",
            "path": "data/Alpaca3-8B/train.jsonl",
            "source_file_sha256": source_sha,
            "license_note": "Use under source dataset license; source attribution retained here"
        },
        "construction": {
            "safe_rule": "exactly one of is_response_0_safe/is_response_1_safe is true",
            "target_rule": "target is the response whose corresponding is_response_*_safe is true",
            "better_response_id_used": False,
            "safer_response_id_used": False,
            "source_split": "train",
            "max_full_tokens": 1024,
            "overlength_policy": "exclude_without_truncation",
            "normalization": "whitespace collapse and casefold for grouping only",
            "group_isolation": "exclude every normalized-prompt group with multiplicity > 1 before selection",
            "selection_seed": args.seed,
            "selection_order": "seeded shuffle of isolated groups, then stable source order",
            "formal_split_isolation": "NOT_ESTABLISHED"
        },
        "counts": dict(counts),
        "pilot": {
            "train_count": len(train),
            "validation_count": len(validation),
            "train_file": str((output_root / "train.jsonl").resolve()),
            "validation_file": str((output_root / "validation.jsonl").resolve()),
            "train_file_sha256": train_sha,
            "validation_file_sha256": validation_sha,
            "all_ids_sha256": sha256_bytes(json.dumps(all_ids, separators=(",", ":")).encode()),
            "train_ids_sha256": sha256_bytes(json.dumps(train_ids, separators=(",", ":")).encode()),
            "validation_ids_sha256": sha256_bytes(json.dumps(validation_ids, separators=(",", ":")).encode()),
            "train_full_tokens": {"min": min(x["full_tokens"] for x in train), "max": max(x["full_tokens"] for x in train), "mean": sum(x["full_tokens"] for x in train) / len(train)},
            "train_target_tokens": {"min": min(x["target_tokens"] for x in train), "max": max(x["target_tokens"] for x in train), "mean": sum(x["target_tokens"] for x in train) / len(train)},
            "validation_full_tokens": {"min": min(x["full_tokens"] for x in validation), "max": max(x["full_tokens"] for x in validation), "mean": sum(x["full_tokens"] for x in validation) / len(validation)},
            "validation_target_tokens": {"min": min(x["target_tokens"] for x in validation), "max": max(x["target_tokens"] for x in validation), "mean": sum(x["target_tokens"] for x in validation) / len(validation)}
        },
        "excluded_line_numbers": {"overlength": overlength, "empty_target": empty_target, "invalid_target_tokens": invalid_tokens},
        "future_exclusion": "all pilot IDs and normalized prompt groups are excluded from formal E1 splits"
    }
    (output_root / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    print(json.dumps({"status": manifest["status"], "counts": manifest["counts"], "pilot": manifest["pilot"], "manifest": str((output_root / "manifest.json").resolve())}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
