from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.harness.env import sha256_bytes, sha256_file


class ArtifactStore:
    """Content-addressed store: any stored blob is placed under a directory named by its sha256 and
    optionally a deterministic logical name. Parentage is recorded in a manifest row."""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.blobs = self.root / "blobs"
        self.blobs.mkdir(exist_ok=True)

    def store_bytes(self, data: bytes, logical_name: str) -> str:
        digest = sha256_bytes(data)
        target = self.blobs / digest[:2] / digest
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            target.write_bytes(data)
        link = self.root / "aliases" / logical_name
        link.parent.mkdir(parents=True, exist_ok=True)
        if not link.exists() and not link.is_symlink():
            try:
                link.symlink_to(target.relative_to(link.parent))
            except (OSError, ValueError):
                link.write_text(digest)
        return digest

    def store_file(self, path: Path, logical_name: str) -> str:
        return self.store_bytes(path.read_bytes(), logical_name)

    def store_dict(self, obj: Any, logical_name: str) -> str:
        import json

        return self.store_bytes(json.dumps(obj, sort_keys=True, indent=2).encode("utf-8"), logical_name)

    def resolve(self, digest_or_alias: str) -> Path | None:
        alias = self.root / "aliases" / digest_or_alias
        if alias.exists():
            if alias.is_symlink():
                return alias.resolve()
            return alias
        candidate = self.blobs / digest_or_alias[:2] / digest_or_alias
        return candidate if candidate.exists() else None

    def manifest_row(self, logical_name: str, digest: str, parent_ids: list[str]) -> dict[str, str]:
        return {"role": "result", "uri": logical_name, "sha256": digest}
