import os
import unittest
from unittest.mock import patch

from browserskill_integration import (
    CapSolverHttpGateway, ChallengeEvent, MockCapSolverGateway, ChallengeCoordinator,
    TaskContext, build_request_help_command, next_browser_action,
)
from browserskill_integration.models import GatewayResult


def context(**changes):
    values = dict(session_id="abcd", tab_id="tab-7", goal="authorized QA", target_url="https://qa.example.test/check", authorization_reference="QA-42", allowed_hosts=frozenset({"qa.example.test"}), max_attempts=1, timeout_seconds=10)
    values.update(changes)
    return TaskContext(**values)


def event(url="https://qa.example.test/check"):
    return ChallengeEvent(True, {"type": "MockTask", "websiteURL": url})


class HandlingTests(unittest.TestCase):
    def test_success_preserves_context(self):
        gateway = MockCapSolverGateway([GatewayResult("ready", {"fixture": "ok"})])
        result = ChallengeCoordinator(gateway).run(context(), event())
        self.assertEqual((result.action, result.session_id, result.tab_id, result.goal), ("resume_once", "abcd", "tab-7", "authorized QA"))
        self.assertEqual(len(gateway.calls), 1)

    def test_missing_authorization_falls_back_without_call(self):
        gateway = MockCapSolverGateway([GatewayResult("ready")])
        result = ChallengeCoordinator(gateway).run(context(authorization_reference=""), event())
        self.assertEqual(result.action, "request_human_help")
        self.assertFalse(gateway.calls)

    def test_denied_host_falls_back(self):
        result = ChallengeCoordinator(MockCapSolverGateway([])).run(context(), event("https://other.example/check"))
        self.assertIn("does not match", result.reason)

    def test_zero_budget_falls_back(self):
        result = ChallengeCoordinator(MockCapSolverGateway([])).run(context(max_attempts=0), event())
        self.assertIn("budget", result.reason)

    def test_provider_error_falls_back(self):
        result = ChallengeCoordinator(MockCapSolverGateway([GatewayResult("error", error_code="TEST_ERROR")])).run(context(), event())
        self.assertEqual(result.action, "request_human_help")
        self.assertIn("TEST_ERROR", result.reason)

    def test_timeout_falls_back(self):
        class TimeoutGateway:
            def solve(self, task, deadline): raise TimeoutError
        result = ChallengeCoordinator(TimeoutGateway()).run(context(), event())
        self.assertIn("timed out", result.reason)

    def test_live_gateway_is_off_by_default(self):
        with patch.dict(os.environ, {}, clear=True):
            result = CapSolverHttpGateway().solve(event().task, 999999999.0)
        self.assertEqual((result.status, result.error_code), ("disabled", "LIVE_MODE_DISABLED"))

    def test_request_help_matches_verified_cli_contract(self):
        criteria = {"any": [{"url_contains": "/accepted"}], "stable_for_ms": 1000}
        command = build_request_help_command(context(), "@e7", criteria)
        self.assertEqual(command[:4], ["bsk", "request-help", "--session", "abcd"])
        self.assertIn("--prompt", command); self.assertIn("--title", command)
        self.assertIn("--target", command); self.assertIn("--completion-criteria", command)

    def test_request_help_omits_unverified_completion_criteria(self):
        command = build_request_help_command(context(), "@e7")
        self.assertNotIn("--completion-criteria", command)

    def test_human_outcomes_are_bounded(self):
        self.assertEqual(next_browser_action("completed", "abcd"), ["bsk", "snapshot", "--session", "abcd"])
        self.assertEqual(next_browser_action("navigated", "abcd"), ["bsk", "session", "stop", "abcd"])
        self.assertEqual(next_browser_action("disabled", "abcd"), ["bsk", "session", "stop", "abcd"])


if __name__ == "__main__":
    unittest.main()
