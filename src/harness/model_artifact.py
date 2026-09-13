from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from src.harness.env import sha256_file, sha256_json


@dataclass(frozen=True)
class ModelArtifact:
    repo_id: str
    revision: str
    tokenizer_repo_id: str
    tokenizer_revision: str
    local_path: Path
    artifact_id: str
    parent_artifact_ids: tuple[str, ...] = ()

    @classmethod
    def from_local(cls, repo_id: str, revision: str, tokenizer_repo_id: str, tokenizer_revision: str, local_path: Path, parent_artifact_ids: tuple[str, ...] = ()) -> "ModelArtifact":
        config_hash = sha256_file(local_path / "config.json") if (local_path / "config.json").exists() else "missing"
        manifest = {
            "repo_id": repo_id,
            "revision": revision,
            "tokenizer_repo_id": tokenizer_repo_id,
            "tokenizer_revision": tokenizer_revision,
            "config_sha256": config_hash,
        }
        artifact_id = sha256_json(manifest)
        return cls(repo_id=repo_id, revision=revision, tokenizer_repo_id=tokenizer_repo_id, tokenizer_revision=tokenizer_revision, local_path=local_path, artifact_id=artifact_id, parent_artifact_ids=tuple(parent_artifact_ids))


class ImmutablePipelineError(RuntimeError):
    pass


class FrozenSealedData:
    """Sealed data handle: stores only hashes and a local pointer, never raw content."""

    def __init__(self, name: str, source_revision: str, file_path: Path, split: str, salt: str):
        self.name = name
        self.source_revision = source_revision
        self.split = split
        self.salt = salt
        self.file_path = file_path
        self.file_sha256 = sha256_file(file_path)

    def as_manifest_field(self) -> dict[str, str]:
        return {
            "name": self.name,
            "source_revision": self.source_revision,
            "file_sha256": self.file_sha256,
            "split": self.split,
            "ids_sha256": "unsealed-local",
        }
