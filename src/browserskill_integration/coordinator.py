from __future__ import annotations

import time
from collections.abc import Callable
from urllib.parse import urlparse

from .gateway import SolvingGateway
from .models import ChallengeEvent, HandlingDecision, TaskContext


class ChallengeCoordinator:
    def __init__(self, gateway: SolvingGateway, clock: Callable[[], float] = time.monotonic) -> None:
        self.gateway = gateway
        self.clock = clock

    def _decision(self, context: TaskContext, action: str, reason: str, attempts: int, solution=None):
        return HandlingDecision(
            action, reason, context.session_id, context.tab_id, context.goal, attempts, solution or {}
        )

    def run(self, context: TaskContext, event: ChallengeEvent) -> HandlingDecision:
        if not event.detected:
            return self._decision(context, "continue", "no challenge detected", 0)
        if not context.authorization_reference.strip():
            return self._decision(context, "request_human_help", "authorization evidence is required", 0)
        if context.target_host not in {host.lower() for host in context.allowed_hosts}:
            return self._decision(context, "request_human_help", "target host is not allowlisted", 0)
        if context.max_attempts < 1:
            return self._decision(context, "request_human_help", "handling budget is exhausted", 0)
        task_url = str(event.task.get("websiteURL", ""))
        if urlparse(task_url).hostname != context.target_host:
            return self._decision(context, "request_human_help", "task URL does not match task context", 0)

        deadline = self.clock() + max(0.0, context.timeout_seconds)
        try:
            result = self.gateway.solve(event.task, deadline)
        except TimeoutError:
            return self._decision(context, "request_human_help", "handling timed out", 1)
        except Exception:
            return self._decision(context, "request_human_help", "handling provider error", 1)
        if result.status == "ready":
            return self._decision(context, "resume_once", "handling result is ready", 1, result.solution)
        return self._decision(
            context, "request_human_help", f"handling stopped: {result.error_code or result.status}", 1
        )
