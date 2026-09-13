from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


class AttackAdapter(ABC):
    """Attack adapter registry. The agent implements one no-op round trip and the machine-readable
    boundary check; actual attack families (A1-A6) are executed only by the authorized executor."""

    family: str

    @abstractmethod
    def register(self) -> None: ...

    @abstractmethod
    def noop(self) -> dict[str, Any]:
        """Must return a dict that survives a round trip unchanged; proves the registry is wired."""

    def requires_authorized_executor(self) -> str:
        return f"attack family {self.family} execution requires authorized executor; blocked, not proxied"


class DefenseAdapter(ABC):
    family: str

    @abstractmethod
    def register(self) -> None: ...

    @abstractmethod
    def noop(self) -> dict[str, Any]: ...


class NoopAttackAdapter(AttackAdapter):
    family = "noop-a0"

    def register(self) -> None:
        return None

    def noop(self) -> dict[str, Any]:
        return {"family": self.family, "payload": "noop-round-trip"}


class NoopDefenseAdapter(DefenseAdapter):
    family = "noop-defense"

    def register(self) -> None:
        return None

    def noop(self) -> dict[str, Any]:
        return {"family": self.family, "payload": "noop-round-trip"}


class BoundaryGuard:
    """Machine-readable train/select/test boundary enforcement for adapters (H4 pass criterion)."""

    ALLOWED_SPLITS = ("train", "attack_dev", "mechanism_dev", "validation", "sealed_test", "utility")

    def assert_split_allowed(self, split: str) -> None:
        if split not in self.ALLOWED_SPLITS:
            raise ValueError(f"illegal split {split!r}; allowed {self.ALLOWED_SPLITS}")

    def assert_test_blind(self, data_name: str, split: str) -> None:
        if split not in ("validation", "sealed_test"):
            return
        normalized = data_name.lower().replace("-", "_")
        if "attack_dev" in normalized or "mechanism_dev" in normalized:
            raise ValueError(f"dev-family data may not enter sealed split: {data_name}")
