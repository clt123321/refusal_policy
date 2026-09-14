#!/usr/bin/env python3
"""V6 E1 orchestration CLI.

This module only orchestrates frozen stages, validates provenance/gates, stores
aggregate artifacts, and records costs. Attack, harmful evaluation, and model
intervention behavior are injected through ExecutorBackend; they are not
implemented here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Protocol

EXPECTED_EXECUTION_SHA = "6a3ab37c078b25197557fe052a027697f8006252"
EXPECTED_RESEARCH_BASE_SHA = "90cf38bb632c0e6ca861596a59dec4acba23f8ba"
VERDICTS = {
    "V6_E1_PASS_REQUIRES_HUMAN_REVIEW",
    "V6_E1_FAIL",
    "V6_E1_INCONCLUSIVE",
    "V6_E1_INVALID",
}
STAGES = ("pilot", "construct", "qualify", "reattack", "plasticity", "verdict")


class GateError(RuntimeError):
    pass


class ExecutorBackend(Protocol):
    def pilot(self, context: "RunContext") -> dict[str, Any]: ...
    def construct(self, context: "RunContext") -> dict[str, Any]: ...
    def qualify(self, context: "RunContext") -> dict[str, Any]: ...
    def reattack(self, context: "RunContext") -> dict[str, Any]: ...
    def plasticity(self, context: "RunContext") -> dict[str, Any]: ...
    def verdict(self, context: "RunContext") -> dict[str, Any]: ...


@dataclass
class RunContext:
    run_dir: Path
    execution_sha: str
    research_base_sha: str
    release_metadata_sha: str | None
    input_artifacts: dict[str, str]
    dry_run: bool = False
    state: dict[str, Any] = field(default_factory=dict)


@dataclass
class RepoGuard:
    execution_sha: str = EXPECTED_EXECUTION_SHA
    git_dir: Path = Path(".")

    def check(self) -> dict[str, str]:
        status = subprocess.run(
            ["git", "status", "--porcelain"], cwd=self.git_dir, check=True,
            capture_output=True, text=True,
        ).stdout
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=self.git_dir, check=True,
            capture_output=True, text=True,
        ).stdout.strip()
        if status.strip():
            raise GateError("EXECUTION_SHA_MISMATCH: working tree is not clean")
        if head != self.execution_sha:
            raise GateError(
                f"EXECUTION_SHA_MISMATCH: expected {self.execution_sha}, got {head}"
            )
        return {"execution_sha": head, "working_tree": "clean"}


class ArtifactVerifier:
    @staticmethod
    def sha256(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1 << 20), b""):
                digest.update(chunk)
        return digest.hexdigest()

    @classmethod
    def verify(cls, artifacts: dict[str, str]) -> None:
        for raw_path, expected in artifacts.items():
            path = Path(raw_path)
            if not path.is_file():
                raise GateError(f"INPUT_ARTIFACT_MISSING: {path}")
            actual = cls.sha256(path)
            if actual != expected:
                raise GateError(
                    f"INPUT_ARTIFACT_HASH_MISMATCH: {path}: expected {expected}, got {actual}"
                )


class JsonArtifactStore:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def write(self, name: str, payload: dict[str, Any]) -> str:
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        encoded = json.dumps(payload, sort_keys=True, indent=2).encode()
        path.write_bytes(encoded)
        return hashlib.sha256(encoded).hexdigest()


class GateState:
    def __init__(self, path: Path):
        self.path = path
        self.data = json.loads(path.read_text()) if path.exists() else {
            "stages": {}, "execution_sha": None, "research_base_sha": None,
        }

    def require_execution(self, execution_sha: str) -> None:
        if self.data.get("execution_sha") not in (None, execution_sha):
            raise GateError("STATE_EXECUTION_SHA_MISMATCH")
        self.data["execution_sha"] = execution_sha

    def require_stage(self, stage: str) -> None:
        if stage == "pilot":
            return
        if not self.data["stages"].get("pilot", {}).get("valid", False):
            raise GateError("PILOT_GATE_NOT_PASSED")
        if stage == "construct" and not self.data["stages"].get("pilot", {}).get("frozen", False):
            raise GateError("PILOT_FIELDS_NOT_FROZEN")
        if stage == "qualify" and not self.data["stages"].get("construct", {}).get("valid", False):
            raise GateError("CONSTRUCT_GATE_NOT_PASSED")
        if stage in ("reattack", "plasticity") and not self.data["stages"].get("qualify", {}).get("valid", False):
            raise GateError("QUALIFICATION_GATE_NOT_PASSED")
        if stage == "verdict":
            for required in ("pilot", "construct", "qualify", "reattack", "plasticity"):
                if not self.data["stages"].get(required, {}).get("valid", False):
                    raise GateError(f"STAGE_GATE_NOT_PASSED: {required}")

    def record(self, stage: str, result: dict[str, Any], artifact_sha: str) -> None:
        self.data["stages"][stage] = {
            "valid": bool(result.get("valid", False)),
            "frozen": bool(result.get("frozen", False)),
            "artifact_sha256": artifact_sha,
            "result": result,
        }

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, sort_keys=True, indent=2))


class MockBenignBackend:
    """Dry-run only. It never runs attack or harmful-evaluation logic."""

    def _result(self, stage: str) -> dict[str, Any]:
        return {
            "stage": stage, "valid": True, "frozen": stage == "pilot",
            "dry_run": True, "executor_backend": "mock-benign",
            "scientific_evidence": False, "cost": {"primary_estimated_flops": 0.0, "trials_attempted": 0},
        }

    def pilot(self, context: RunContext) -> dict[str, Any]: return self._result("pilot")
    def construct(self, context: RunContext) -> dict[str, Any]: return self._result("construct")
    def qualify(self, context: RunContext) -> dict[str, Any]: return self._result("qualify")
    def reattack(self, context: RunContext) -> dict[str, Any]: return self._result("reattack")
    def plasticity(self, context: RunContext) -> dict[str, Any]: return self._result("plasticity")
    def verdict(self, context: RunContext) -> dict[str, Any]:
        return {"stage": "verdict", "valid": True, "verdict": "V6_E1_INVALID", "dry_run": True, "scientific_evidence": False}


def load_backend(spec: str, dry_run: bool) -> ExecutorBackend:
    if dry_run or spec == "mock-benign":
        return MockBenignBackend()
    module_name, separator, attr = spec.partition(":")
    if not separator:
        raise GateError("backend must be MODULE:ATTRIBUTE or mock-benign")
    module = __import__(module_name, fromlist=[attr])
    backend = getattr(module, attr)()
    for stage in STAGES:
        if not callable(getattr(backend, stage, None)):
            raise GateError(f"backend missing stage method: {stage}")
    return backend


def run_stage(stage: str, args: argparse.Namespace) -> dict[str, Any]:
    guard = RepoGuard(args.execution_sha, Path(args.repo))
    repo_info = guard.check()
    ArtifactVerifier.verify(dict(item.split("=", 1) for item in args.input_artifact))
    run_dir = Path(args.run_dir)
    state = GateState(run_dir / "gate_state.json")
    state.require_execution(args.execution_sha)
    state.require_stage(stage)
    context = RunContext(run_dir, args.execution_sha, args.research_base_sha, args.release_metadata_sha, {}, args.dry_run, state.data)
    backend = load_backend(args.backend, args.dry_run)
    result = getattr(backend, stage)(context)
    if not isinstance(result, dict):
        raise GateError(f"backend returned non-dict for {stage}")
    store = JsonArtifactStore(run_dir / "artifacts")
    artifact_sha = store.write(f"{stage}.json", result)
    result["execution_sha"] = args.execution_sha
    result["research_base_sha"] = args.research_base_sha
    result["release_metadata_sha"] = args.release_metadata_sha
    result["repo_check"] = repo_info
    state.record(stage, result, artifact_sha)
    state.save()
    print(json.dumps({"stage": stage, "artifact_sha256": artifact_sha, "result": result}, indent=2))
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="V6 E1 orchestration only; attacks/evaluator are injected backends")
    parser.add_argument("--repo", default=".")
    parser.add_argument("--execution-sha", default=EXPECTED_EXECUTION_SHA)
    parser.add_argument("--research-base-sha", default=EXPECTED_RESEARCH_BASE_SHA)
    parser.add_argument("--release-metadata-sha", default=None)
    parser.add_argument("--run-dir", default="artifacts/v6_e1_executor")
    parser.add_argument("--backend", default="mock-benign")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--input-artifact", action="append", default=[], metavar="PATH=SHA256")
    sub = parser.add_subparsers(dest="stage", required=True)
    for stage in STAGES:
        sub.add_parser(stage)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        run_stage(args.stage, args)
    except (GateError, ValueError, ImportError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
