import json
from pathlib import Path
import pytest
from src.execution.repair_runner import run_repair


def test_repair_runner_requires_frozen_config(tmp_path):
    config = {"data": {}, "objective": {"status": "PENDING"}}
    p = tmp_path / "config.json"; p.write_text(json.dumps(config))
    with pytest.raises(ValueError, match="REPAIR_CONFIG_NOT_FROZEN"):
        run_repair(p, tmp_path, tmp_path / "out", "cpu")


def test_repair_runner_requires_data_rows_and_hash(tmp_path):
    data = tmp_path / "repair.jsonl"; data.write_text(json.dumps({"prompt":"x", "target":"y"})+"\n")
    cfg = {"data":{"path":str(data),"file_sha256":"bad","ids_sha256":"x"},"objective":{"status":"FROZEN"},"trainable":{"parameterization":"x","status":"FROZEN"},"optimizer":{"status":"FROZEN"},"schedule":{"status":"FROZEN"}}
    p=tmp_path/'config.json'; p.write_text(json.dumps(cfg))
    with pytest.raises(ValueError, match="D_REPAIR_HASH_MISMATCH"):
        run_repair(p, tmp_path, tmp_path/'out','cpu')
