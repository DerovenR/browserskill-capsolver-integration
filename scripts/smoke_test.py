from browserskill_integration import ChallengeEvent, MockCapSolverGateway, ChallengeCoordinator, TaskContext
from browserskill_integration.models import GatewayResult

context = TaskContext("abcd", "tab-1", "authorized QA", "https://qa.example.test/check", "QA-1", frozenset({"qa.example.test"}))
event = ChallengeEvent(True, {"type": "MockTask", "websiteURL": context.target_url})
decision = ChallengeCoordinator(MockCapSolverGateway([GatewayResult("ready", {"fixture": "ok"})])).run(context, event)
assert decision.action == "resume_once"
assert decision.session_id == "abcd" and decision.tab_id == "tab-1"
print("SMOKE PASSED: authorized fixture completed once; BrowserSkill context preserved")
