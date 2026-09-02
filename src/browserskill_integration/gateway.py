from __future__ import annotations

import json
import os
import time
import urllib.request
from collections.abc import Callable, Mapping
from typing import Any, Protocol

from .models import GatewayResult

CREATE_TASK_URL = "https://api.capsolver.com/createTask"
GET_RESULT_URL = "https://api.capsolver.com/getTaskResult"


class SolvingGateway(Protocol):
    def solve(self, task: Mapping[str, Any], deadline: float) -> GatewayResult: ...


class MockCapSolverGateway:
    """Deterministic fixture gateway; it never uses the network."""

    def __init__(self, results: list[GatewayResult]) -> None:
        self.results = list(results)
        self.calls: list[Mapping[str, Any]] = []

    def solve(self, task: Mapping[str, Any], deadline: float) -> GatewayResult:
        self.calls.append(task)
        if not self.results:
            return GatewayResult("error", error_code="MOCK_RESULT_MISSING")
        return self.results.pop(0)


class CapSolverHttpGateway:
    """Small official-API client, disabled unless live use is explicitly enabled."""

    def __init__(self, *, api_key: str | None = None, poll_interval: float = 3.0,
                 max_polls: int = 120,
                 opener: Callable[[urllib.request.Request, float], Mapping[str, Any]] | None = None) -> None:
        self.api_key = api_key or os.getenv("CAPSOLVER_API_KEY", "")
        self.poll_interval = poll_interval
        self.max_polls = min(max_polls, 120)
        self._opener = opener or self._post

    @staticmethod
    def _post(request: urllib.request.Request, timeout: float) -> Mapping[str, Any]:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))

    def _request(self, url: str, payload: Mapping[str, Any], deadline: float) -> Mapping[str, Any]:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("handling deadline reached")
        request = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                                         headers={"Content-Type": "application/json"}, method="POST")
        return self._opener(request, min(remaining, 15.0))

    def solve(self, task: Mapping[str, Any], deadline: float) -> GatewayResult:
        if os.getenv("CAPSOLVER_ALLOW_LIVE") != "1":
            return GatewayResult("disabled", error_code="LIVE_MODE_DISABLED")
        if not self.api_key:
            return GatewayResult("disabled", error_code="API_KEY_MISSING")
        if not isinstance(task.get("type"), str) or not isinstance(task.get("websiteURL"), str):
            return GatewayResult("error", error_code="INVALID_TASK_CONTRACT")
        created = self._request(CREATE_TASK_URL, {"clientKey": self.api_key, "task": dict(task)}, deadline)
        if int(created.get("errorId", 0)) > 0:
            return GatewayResult("error", error_code=str(created.get("errorCode", "CREATE_ERROR")))
        if created.get("status") == "ready":
            return GatewayResult("ready", solution=created.get("solution", {}))
        task_id = created.get("taskId")
        if not task_id:
            return GatewayResult("error", error_code="TASK_ID_MISSING")
        for _ in range(self.max_polls):
            if time.monotonic() + self.poll_interval > deadline:
                return GatewayResult("timeout", error_code="HANDLING_TIMEOUT")
            time.sleep(self.poll_interval)
            result = self._request(GET_RESULT_URL, {"clientKey": self.api_key, "taskId": task_id}, deadline)
            if int(result.get("errorId", 0)) > 0:
                return GatewayResult("error", error_code=str(result.get("errorCode", "RESULT_ERROR")))
            if result.get("status") == "ready":
                return GatewayResult("ready", solution=result.get("solution", {}))
        return GatewayResult("timeout", error_code="POLL_BUDGET_EXHAUSTED")
