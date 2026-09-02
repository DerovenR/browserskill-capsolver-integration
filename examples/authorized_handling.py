from browserskill_integration import ChallengeEvent, MockCapSolverGateway, ChallengeCoordinator, TaskContext
from browserskill_integration.models import GatewayResult

context = TaskContext(
    session_id="abcd", tab_id="tab-1", goal="verify owned checkout QA",
    target_url="https://qa.example.test/checkout", authorization_reference="QA-2026-08-20",
    allowed_hosts=frozenset({"qa.example.test"}),
)
event = ChallengeEvent(True, {"type": "OfficialTaskTypeFromCurrentDocs", "websiteURL": context.target_url})
decision = ChallengeCoordinator(MockCapSolverGateway([GatewayResult("ready", {"mock": True})])).run(context, event)
print(f"{decision.action}: {decision.reason}")
