import json
from pathlib import Path
import pytest
from src.execution.repair_runner import _require_executable, build_parser, load_jsonl_repair_data, run_repair


def test_repair_runner_requires_frozen_config(tmp_path):
    config = {"data": {}, "objective": {"status": "PENDING"}}
    p = tmp_path / "config.json"; p.write_text(json.dumps(config))
    with pytest.raises(ValueError, match="REPAIR_CONFIG_NOT_EXECUTABLE"):
        run_repair(
            p, tmp_path, tmp_path / "out", "cpu", execution_sha="0" * 40,
            task_id="t", run_id="r", attempt_id="a",
        )


def test_repair_runner_requires_data_rows_and_hash(tmp_path):
    data = tmp_path / "repair.jsonl"; data.write_text(json.dumps({"id":"1", "prompt":"x", "target":"y"})+"\n")
    cfg = {
        "mode":"DEV", "scientific_evidence":False,
        "data":{"path":str(data),"file_sha256":"bad","ids_sha256":"x"},
        "objective":{"status":"DEV_LOCKED"},
        "trainable":{"parameterization":"x","status":"DEV_LOCKED"},
        "optimizer":{"status":"DEV_LOCKED"},
        "schedule":{"steps":1,"batch_size":1,"gradient_accumulation_steps":1,"checkpoint_steps":[0,1],"status":"DEV_LOCKED"},
        "lineage":{"parent_artifact_id":"dev-base","arm":"DEV"},
    }
    p=tmp_path/'config.json'; p.write_text(json.dumps(cfg))
    with pytest.raises(ValueError, match="D_REPAIR_HASH_MISMATCH"):
        run_repair(
            p, tmp_path, tmp_path/'out','cpu', execution_sha="0" * 40,
            task_id="t", run_id="r", attempt_id="a",
        )


def test_tracked_dev_config_is_executable_but_not_scientific():
    config = json.loads(Path("configs/execution/v6_repair_dev.json").read_text())
    _require_executable(config)
    assert config["mode"] == "DEV"
    assert config["scientific_evidence"] is False
    rows = load_jsonl_repair_data(Path(config["data"]["path"]))
    assert [row["id"] for row in rows] == ["dev-repair-001", "dev-repair-002"]


def test_repair_cli_requires_distinct_run_identity():
    args = build_parser().parse_args([
        "--config", "configs/execution/v6_repair_dev.json",
        "--parent-model", "/model", "--output", "/out",
        "--execution-sha", "a" * 40, "--task-id", "V6.E1.DEV.REPAIR_GPU_SMOKE",
        "--run-id", "V6.E1.DEV.REPAIR_GPU_SMOKE.s17", "--attempt-id", "V6.E1.DEV.REPAIR_GPU_SMOKE.s17.a01",
    ])
    assert args.run_id != args.attempt_id
