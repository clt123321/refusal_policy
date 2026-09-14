import json
from pathlib import Path

import pytest

from src.harness.e1_isolation import E1_SPLITS, isolate_record_ids, validate_isolation


def test_isolate_ids_salted_and_deterministic():
    ids = ["a", "b"]
    out1 = isolate_record_ids(ids, "salt")
    out2 = isolate_record_ids(ids, "salt")
    assert out1 == out2
    assert out1[0] != "a"
    assert isolate_record_ids(["a"], "s1") != isolate_record_ids(["a"], "s2")


def test_validate_isolation_no_overlap(tmp_path):
    files = {}
    for i, split in enumerate(E1_SPLITS):
        p = tmp_path / f"{split}.txt"
        p.write_text("\n".join(f"id-{split}-{j}" for j in range(10)))
        files[split] = p
    result = validate_isolation(files)
    assert result["pass"] is True
    assert result["split_overlaps"] == {}


def test_validate_isolation_detects_overlap(tmp_path):
    files = {}
    for i, split in enumerate(E1_SPLITS):
        p = tmp_path / f"{split}.txt"
        p.write_text("\n".join(f"id-{split}-{j}" for j in range(10)))
        files[split] = p
    # inject a duplicate into one other split
    files["D_A1_train"].write_text("id-D_A0_loc-3\nid-D_A1_train-0\n")
    result = validate_isolation(files)
    assert result["pass"] is False
    assert "D_A0_loc|D_A1_train" in result["split_overlaps"]


def test_validate_isolation_rejects_missing(tmp_path):
    files = {split: (tmp_path / f"{split}.txt") for split in E1_SPLITS[:4]}
    result = validate_isolation(files)
    assert result["pass"] is False
    assert "missing splits" in result["error"]
