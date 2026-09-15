from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from scripts.build_v6_repair_pilot_data import normalize_text, row_id, tokenized_example


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--tokenizer", type=Path, required=True)
    parser.add_argument("--exclude-manifest", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--max-full-tokens", type=int, default=1024)
    args = parser.parse_args()
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer.as_posix())
    excluded_manifest = json.loads(args.exclude_manifest.read_text())
    excluded_ids = set()
    for key in ("train_file", "validation_file"):
        path = Path(excluded_manifest["pilot"][key])
        excluded_ids.update(json.loads(line)["id"] for line in path.read_text().splitlines() if line.strip())
    candidates = []
    counts = Counter()
    source_sha = hashlib.sha256(args.source.read_bytes()).hexdigest()
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
            prompt = row.get("prompt")
            target = row.get(response_key)
            if not isinstance(prompt, str) or not prompt.strip() or not isinstance(target, str) or not target.strip():
                counts["excluded_empty_prompt_or_target"] += 1
                continue
            full_tokens, target_tokens = tokenized_example(tokenizer, prompt, target)
            if target_tokens <= 0:
                counts["excluded_zero_target_tokens"] += 1
                continue
            if full_tokens > args.max_full_tokens:
                counts["excluded_overlength"] += 1
                continue
            target_sha = row.get(f"{response_key}_sha256")
            item_id = row_id(prompt, target, str(target_sha or ""))
            if item_id in excluded_ids:
                counts["excluded_prior_dev_ids"] += 1
                continue
            candidates.append({"id": item_id, "prompt": prompt, "target": target, "source_line": line_number, "source_target_field": response_key, "source_target_sha256": target_sha, "prompt_norm": normalize_text(prompt), "full_tokens": full_tokens, "target_tokens": target_tokens})
    by_id = {item["id"]: item for item in candidates}
    counts["excluded_duplicate_ids"] = len(candidates) - len(by_id)
    grouped = Counter(item["prompt_norm"] for item in by_id.values())
    counts["duplicate_prompt_groups"] = sum(v > 1 for v in grouped.values())
    counts["duplicate_prompt_rows"] = sum(v - 1 for v in grouped.values() if v > 1)
    isolated = [item for item in by_id.values() if grouped[item["prompt_norm"]] == 1]
    counts["eligible_group_isolated"] = len(isolated)
    isolated.sort(key=lambda item: item["id"])
    for item in isolated:
        item.pop("prompt_norm", None)
    args.output_root.mkdir(parents=True, exist_ok=True)
    output = args.output_root / "candidate_pool.jsonl"
    encoded = b"".join((json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n").encode() for item in isolated)
    output.write_bytes(encoded)
    ids = [item["id"] for item in isolated]
    manifest = {"dataset_id": "V6.E1.D_REPAIR_CANDIDATE_POOL", "status": "CANDIDATE_NOT_FORMAL", "source": {"repo_id": "PKU-Alignment/PKU-SafeRLHF", "repo_type": "dataset", "revision": "9421ffafec3fa40a1f1a7d567b4d525079477ecb", "path": "data/Alpaca3-8B/train.jsonl", "source_file_sha256": source_sha}, "excluded_prior_dev": {"manifest": str(args.exclude_manifest.resolve()), "count": len(excluded_ids), "rule": "exclude all prior DEV train and validation IDs"}, "construction": {"safe_rule": "exactly one safe annotation true", "target_rule": "take corresponding raw response", "better_response_id_used": False, "safer_response_id_used": False, "max_full_tokens": args.max_full_tokens, "overlength_policy": "exclude_without_truncation", "normalization": "whitespace collapse and casefold for grouping only", "group_isolation": "remove all prompt groups with multiplicity greater than one", "formal_split_isolation": "NOT_ESTABLISHED"}, "counts": dict(counts), "candidate_pool": {"count": len(isolated), "path": str(output.resolve()), "file_sha256": hashlib.sha256(encoded).hexdigest(), "ids_sha256": hashlib.sha256(json.dumps(ids, separators=(",", ":")).encode()).hexdigest(), "recommended_split": {"train": 2048, "validation": 256, "reserve": max(0, len(isolated) - 2304)}}, "future_exclusion": "exclude candidate pool IDs and prompt groups from formal E1 splits until final split plan is frozen"}
    (args.output_root / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    print(json.dumps({"manifest": str((args.output_root / "manifest.json").resolve()), "counts": dict(counts), "candidate_count": len(isolated), "file_sha256": manifest["candidate_pool"]["file_sha256"], "ids_sha256": manifest["candidate_pool"]["ids_sha256"]}, ensure_ascii=False, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
