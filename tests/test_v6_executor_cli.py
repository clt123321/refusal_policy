import json
import subprocess
from pathlib import Path

import pytest

from scripts.v6_e1_executor import (
    GateError,
    GateState,
    MockBenignBackend,
    RepoGuard,
    build_parser,
    main,
    run_stage,
)


def init_repo(path: Path, clean=True):
    subprocess.run(["git", "init", "-q"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.name", "test"], cwd=path, check=True)
    (path / "file.txt").write_text("x")
    subprocess.run(["git", "add", "file.txt"], cwd=path, check=True)
    subprocess.run(["git", "commit", "-qm", "init"], cwd=path, check=True)
    if not clean:
        (path / "dirty.txt").write_text("dirty")


def test_repo_guard_rejects_dirty_tree(tmp_path):
    init_repo(tmp_path, clean=False)
    with pytest.raises(GateError, match="EXECUTION_SHA_MISMATCH"):
        RepoGuard(subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=tmp_path, text=True).strip(), tmp_path).check()


def test_repo_guard_rejects_wrong_sha(tmp_path):
    init_repo(tmp_path)
    with pytest.raises(GateError, match="EXECUTION_SHA_MISMATCH"):
        RepoGuard("0" * 40, tmp_path).check()


def test_gate_state_requires_order(tmp_path):
    state = GateState(tmp_path / "state.json")
    state.require_execution("a" * 40)
    with pytest.raises(GateError, match="PILOT_GATE_NOT_PASSED"):
        state.require_stage("construct")
    state.record("pilot", {"valid": True, "frozen": True}, "a" * 64)
    state.require_stage("construct")


def test_gate_state_allows_terminal_invalid_verdict(tmp_path):
    state = GateState(tmp_path / "state.json")
    state.record("pilot", {"valid": True, "frozen": True}, "a" * 64)
    state.record("construct", {"valid": True}, "b" * 64)
    state.record("qualify", {"valid": False, "classification": "MATCHING_FAILED"}, "c" * 64)
    state.require_stage("verdict")
    assert "reattack" not in state.data["stages"]
    assert "plasticity" not in state.data["stages"]


def test_mock_backend_never_produces_scientific_evidence():
    backend = MockBenignBackend()
    for stage in ("pilot", "construct", "qualify", "reattack", "plasticity"):
        result = getattr(backend, stage)(None)
        assert result["dry_run"] is True
        assert result["scientific_evidence"] is False
    assert backend.verdict(None)["verdict"] == "V6_E1_INVALID"


def test_parser_has_all_stages():
    parser = build_parser()
    for stage in ("pilot", "construct", "qualify", "reattack", "plasticity", "verdict"):
        args = parser.parse_args(["--dry-run", "--execution-sha", "a" * 40, stage])
        assert args.stage == stage


def test_run_stage_dry_run_gate_and_artifact(tmp_path):
    init_repo(tmp_path)
    current_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=tmp_path, text=True).strip()
    result = run_stage("pilot", type("Args", (), {
        "repo": str(tmp_path), "execution_sha": current_sha,
        "research_base_sha": "r" * 40, "release_metadata_sha": "m" * 40,
        "input_artifact": [], "dry_run": True,
        "run_dir": str(tmp_path / "run"), "backend": "mock-benign",
    })())
    assert result["valid"] is True
    assert (tmp_path / "run" / "artifacts" / "pilot.json").exists()
    artifact = json.loads((tmp_path / "run" / "artifacts" / "pilot.json").read_text())
    assert artifact["execution_sha"] == current_sha
    state = json.loads((tmp_path / "run" / "gate_state.json").read_text())
    assert state["stages"]["pilot"]["valid"] is True


def test_run_stage_blocks_out_of_order(tmp_path):
    init_repo(tmp_path)
    current_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=tmp_path, text=True).strip()
    args = type("Args", (), {
        "repo": str(tmp_path), "execution_sha": current_sha,
        "research_base_sha": "r" * 40, "release_metadata_sha": None,
        "input_artifact": [], "dry_run": True,
        "run_dir": str(tmp_path / "run"), "backend": "mock-benign",
    })()
    with pytest.raises(GateError, match="PILOT_GATE_NOT_PASSED"):
        run_stage("construct", args)


def test_cli_returns_error_for_execution_sha_mismatch(tmp_path):
    init_repo(tmp_path)
    code = main(["--repo", str(tmp_path), "--execution-sha", "0" * 40, "--dry-run", "pilot"])
    assert code == 2
