from __future__ import annotations

import json

from .models import TaskContext


def build_request_help_command(context: TaskContext, target: str | None = None) -> list[str]:
    command = [
        "bsk", "request-help", "--session", context.session_id,
        "--prompt", "Please complete the visible checkpoint, or cancel to stop the task.",
        "--title", "Human review required",
        "--timeout", f"{context.human_help_timeout_seconds}s",
    ]
    if target:
        command.extend(["--target", target])
    command.extend([
        "--completion-criteria",
        json.dumps({"type": "user_confirm", "description": "Checkpoint reviewed"}, separators=(",", ":")),
    ])
    return command


def next_browser_action(outcome: str, session_id: str) -> list[str]:
    if outcome in {"continued", "completed", "navigated"}:
        return ["bsk", "snapshot", "--session", session_id]
    return ["bsk", "session", "stop", session_id]
