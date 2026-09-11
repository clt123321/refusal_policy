import json
from collections import Counter
from pathlib import Path

OUT_DIR = Path("artifacts/safe_mech")


def transitions(baseline_rows, treated_rows):
    baseline_by_id = {r["example_id"]: r for r in baseline_rows}
    treated_by_id = {r["example_id"]: r for r in treated_rows}
    counts = Counter()
    rows = []
    for example_id, base in baseline_by_id.items():
        treat = treated_by_id.get(example_id)
        if treat is None:
            continue
        base_state = "abstain" if base["is_abstain"] else ("invalid" if base["label"] == "invalid" else "compliant")
        treat_state = "abstain" if treat["is_abstain"] else ("invalid" if treat["label"] == "invalid" else "compliant")
        key = f"{base_state}->{treat_state}"
        counts[key] += 1
        rows.append({"example_id": example_id, "baseline_label": base["label"], "treated_label": treat["label"], "transition": key})
    return counts, rows


def main() -> None:
    multilayer = [json.loads(line) for line in (OUT_DIR / "raw_completions_multilayer.jsonl").read_text().splitlines()]
    by_cond = {}
    for r in multilayer:
        by_cond.setdefault(r["condition"], []).append(r)

    remove_counts, remove_rows = transitions(by_cond["baseline_abstain"], by_cond["remove"])
    add_counts, add_rows = transitions(by_cond["baseline_natural"], by_cond["add"])

    def rate(rows, key):
        return sum(1 for r in rows if r[key]) / len(rows)

    summary = {
        "role": "SAFE_MECH_BENIGN_PROXY",
        "remove_condition": {
            "n": len(by_cond["baseline_abstain"]),
            "baseline_abstain_rate": rate(by_cond["baseline_abstain"], "is_abstain"),
            "after_remove_abstain_rate": rate(by_cond["remove"], "is_abstain"),
            "transition_counts": dict(remove_counts),
        },
        "add_condition": {
            "n": len(by_cond["baseline_natural"]),
            "baseline_abstain_rate": rate(by_cond["baseline_natural"], "is_abstain"),
            "after_add_abstain_rate": rate(by_cond["add"], "is_abstain"),
            "transition_counts": dict(add_counts),
        },
    }
    Path(OUT_DIR / "baseline_transition_tables.json").write_text(json.dumps(summary, indent=2))
    Path(OUT_DIR / "baseline_transition_remove.jsonl").write_text("\n".join(json.dumps(r) for r in remove_rows) + "\n")
    Path(OUT_DIR / "baseline_transition_add.jsonl").write_text("\n".join(json.dumps(r) for r in add_rows) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
