from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping
from urllib.parse import urlparse


@dataclass(frozen=True)
class TaskContext:
    session_id: str
    tab_id: str
    goal: str
    target_url: str
    authorization_reference: str
    allowed_hosts: frozenset[str]
    max_attempts: int = 1
    timeout_seconds: float = 30.0
    human_help_timeout_seconds: int = 300

    @property
    def target_host(self) -> str:
        return (urlparse(self.target_url).hostname or "").lower()


@dataclass(frozen=True)
class ChallengeEvent:
    detected: bool
    task: Mapping[str, Any] = field(default_factory=dict)
    marker: str = "challenge-detected"


@dataclass(frozen=True)
class GatewayResult:
    status: str
    solution: Mapping[str, Any] = field(default_factory=dict)
    error_code: str = ""


@dataclass(frozen=True)
class RecoveryDecision:
    action: str
    reason: str
    session_id: str
    tab_id: str
    goal: str
    attempts_used: int
    solution: Mapping[str, Any] = field(default_factory=dict)
