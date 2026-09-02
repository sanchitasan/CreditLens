from app.agents.factory import (
    create_creditlens_orchestrator,
)
from app.agents.orchestrator import (
    CreditLensOrchestrator,
)


def test_create_creditlens_orchestrator():

    orchestrator = (
        create_creditlens_orchestrator()
    )

    assert isinstance(
        orchestrator,
        CreditLensOrchestrator,
    )

    assert orchestrator.financial_agent is not None
    assert orchestrator.risk_agent is not None
    assert orchestrator.policy_agent is not None
    assert (
        orchestrator.final_analyst_agent
        is not None
    )