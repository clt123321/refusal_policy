from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import jsonschema

from src.harness.env import sha256_json


class ManifestValidationError(ValueError):
    pass


PROTOCOL_SCHEMA_PATH = Path("research/protocols/V4_PROTOCOL_SCHEMA.json")
RESULT_SCHEMA_PATH = Path("research/protocols/V4_RESULT_SCHEMA.json")


def load_schema(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"schema not found: {path}")
    return json.loads(path.read_text())


def validate_manifest(manifest: dict[str, Any], schema_path: Path = PROTOCOL_SCHEMA_PATH) -> None:
    schema = load_schema(schema_path)
    try:
        jsonschema.validate(instance=manifest, schema=schema)
    except jsonschema.ValidationError as exc:
        raise ManifestValidationError(f"manifest failed {schema_path.name}: {exc.message}") from exc


def validate_result_card(card: dict[str, Any], schema_path: Path = RESULT_SCHEMA_PATH) -> None:
    schema = load_schema(schema_path)
    try:
        jsonschema.validate(instance=card, schema=schema)
    except jsonschema.ValidationError as exc:
        raise ManifestValidationError(f"result card failed {schema_path.name}: {exc.message}") from exc


def build_run_manifest(*, run_id: str, stage: str, repo_commit: str, environment: dict[str, str], model: dict[str, Any], data: list[dict[str, str]], config: dict[str, Any], seed: int, hardware: dict[str, Any], cost: dict[str, Any], status: str, artifacts: list[dict[str, str]], censoring: str = "none") -> dict[str, Any]:
    manifest = {
        "schema_version": "4.0.0",
        "run_id": run_id,
        "stage": stage,
        "change_card_id": None,
        "repo_commit": repo_commit,
        "environment": environment,
        "model": model,
        "data": data,
        "config_sha256": sha256_json(config),
        "seed": seed,
        "hardware": hardware,
        "cost": cost,
        "status": status,
        "censoring": censoring,
        "artifacts": artifacts,
    }
    validate_manifest(manifest)
    return manifest
