import app.agents.policy_analyst_agent as agent_module
from app.agents.policy_analyst_agent import (
    PolicyAnalystAgent,
    PolicyAnalystInput,
)


def test_policy_agent_delegates_to_policy_tool(monkeypatch):

    received = {}

    def fake_policy_tool(
        foir,
        credit_score,
        previous_defaults,
        default_probability,
        lending_decision,
    ):
        received["foir"] = foir
        received["credit_score"] = credit_score
        received["previous_defaults"] = previous_defaults
        received["default_probability"] = default_probability
        received["lending_decision"] = lending_decision

        return "Retrieved FOIR and credit score policy guidance."

    monkeypatch.setattr(
        agent_module,
        "policy_retrieval_tool",
        fake_policy_tool,
    )

    agent = PolicyAnalystAgent()

    result = agent.analyze(
        PolicyAnalystInput(
            foir=25.0,
            credit_score=780,
            previous_defaults=0,
            default_probability=0.03,
            lending_decision="APPROVE",
        )
    )

    assert received == {
        "foir": 25.0,
        "credit_score": 780,
        "previous_defaults": 0,
        "default_probability": 0.03,
        "lending_decision": "APPROVE",
    }

    assert result.policy_context == (
        "Retrieved FOIR and credit score policy guidance."
    )


def test_policy_agent_returns_policy_analysis(monkeypatch):

    monkeypatch.setattr(
        agent_module,
        "policy_retrieval_tool",
        lambda **kwargs: "Policy context",
    )

    agent = PolicyAnalystAgent()

    result = agent.analyze(
        PolicyAnalystInput(
            foir=58.0,
            credit_score=680,
            previous_defaults=2,
            default_probability=0.28,
            lending_decision="REJECT",
        )
    )

    assert result.policy_context == "Policy context"