---
name: browserskill-capsolver-recovery
description: Apply one bounded recovery attempt to an authorized BrowserSkill task, then use BrowserSkill human help or stop.
---

# BrowserSkill CapSolver recovery companion

Use this companion only for public, owned, or explicitly authorized targets.

1. Start the official lifecycle with `bsk session start` and retain the returned four-letter session ID.
2. Observe with `bsk observe --session <id>`; use `bsk snapshot --session <id>` only when needed.
3. When a challenge is detected, construct `TaskContext` with the same session, tab, goal, target URL, written authorization reference, host allowlist, one-attempt budget, and deadline.
4. Call `RecoveryCoordinator.run`. Do not invent provider task fields; pass only a task contract verified against current official CapSolver documentation.
5. On `resume_once`, apply the returned result only through target-owner-approved code, then take one fresh snapshot. This repository deliberately does not implement page-specific result application.
6. On every other recovery outcome, build the exact foreground fallback with `build_request_help_command`. Treat `cancelled`, `timed_out`, or `disabled` as stop conditions. After `continued` or `completed`, take one fresh snapshot.
7. Always finish with `bsk session stop <id>`.

Never raise budgets automatically, retry `disabled`, collect credentials, hide automation, or continue after an authorization or host mismatch.
