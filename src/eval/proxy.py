from typing import Any


def evaluate_behavior(rows: list[dict[str, Any]], outputs: list[str]) -> dict[str, float]:
    if len(rows) != len(outputs):
        raise ValueError("rows and outputs must have equal length")
    valid = 0
    abstain = 0
    correct = 0
    lengths = []
    for row, output in zip(rows, outputs):
        text = output.strip().lower()
        valid += bool(text)
        abstain += any(token in text for token in ("abstain", "cannot", "decline"))
        correct += row["action"] in text
        lengths.append(len(output.split()))
    n = len(rows)
    return {"policy_choice_rate": abstain / n, "task_correctness": correct / n, "valid_output_rate": valid / n, "mean_generation_length": sum(lengths) / n}
