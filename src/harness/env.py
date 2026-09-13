from __future__ import annotations

import hashlib
import json
import os
import platform
import socket
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_json(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def normalize_record_id(record_id: str, salt: str) -> str:
    import unicodedata

    normalized = unicodedata.normalize("NFKC", record_id).replace("\r\n", "\n").replace("\r", "\n").strip()
    normalized = " ".join(normalized.split())
    return normalized


def salted_record_hash(record_id: str, salt: str) -> str:
    return hashlib.sha256((salt + "||" + normalize_record_id(record_id, salt)).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class EnvironmentLock:
    container_digest: str
    lock_sha256: str
    python: str
    pytorch: str
    transformers: str
    datasets: str
    accelerate: str
    cuda_toolkit: str
    driver: str
    hf_cache_root: str
    hostname_hash: str

    @classmethod
    def capture(cls) -> "EnvironmentLock":
        import platform as _platform

        import accelerate
        import datasets
        import torch
        import transformers

        def _version(pkg: Any) -> str:
            try:
                return pkg.__version__
            except AttributeError:
                return str(pkg)

        container_digest = os.environ.get("CONTAINER_DIGEST", "unset")
        lock_fields = {
            "python": _platform.python_version(),
            "pytorch": _version(torch),
            "transformers": _version(transformers),
            "datasets": _version(datasets),
            "accelerate": _version(accelerate),
            "driver": os.environ.get("NVIDIA_DRIVER_VERSION", "unset"),
            "hf_cache_root": os.environ.get("HF_HOME", os.path.expanduser("~/.cache/huggingface")),
            "hostname": socket.gethostname(),
        }
        lock_sha256 = sha256_json(lock_fields)
        return cls(
            container_digest=container_digest,
            lock_sha256=lock_sha256,
            python=lock_fields["python"],
            pytorch=lock_fields["pytorch"],
            transformers=lock_fields["transformers"],
            datasets=lock_fields["datasets"],
            accelerate=lock_fields["accelerate"],
            cuda_toolkit=torch.version.cuda if torch.version.cuda else "unknown",
            driver=lock_fields["driver"],
            hf_cache_root=lock_fields["hf_cache_root"],
            hostname_hash=sha256_bytes(socket.gethostname().encode("utf-8"))[:16],
        )

    def as_manifest_field(self) -> dict[str, str]:
        return {
            "container_digest": self.container_digest,
            "lock_sha256": self.lock_sha256,
            "python": self.python,
            "pytorch": self.pytorch,
            "cuda": self.cuda_toolkit,
            "driver": self.driver,
        }
