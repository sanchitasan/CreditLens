from types import SimpleNamespace

from app.agents.credit_analyst_agent import (
    CreditAnalystAgent,
    CreditAnalystAgentInput,
)
from app.finance.profile import FinancialProfile


class FakeAnalyst:
    def __init__(self):
        self.received = None

    def analyze(self, application):
        self.received = application

        return "Mock credit analyst explanation."


def create_profile():
    return FinancialProfile(
        monthly_income=80000,
        existing_obligations=20000,
        loan_amount=500000,
        annual_interest_rate=12,
        tenure_years=5,
        credit_score=780,
        employment_years=5,
        previous_defaults=0,
    )


def test_agent_orchestrates_credit_assessment(monkeypatch):

    import app.agents.credit_analyst_agent as agent_module

    fake_analyst = FakeAnalyst()

    assessment = SimpleNamespace(
        foir=25.0,
        emi=11122.22,
        total_obligations=31122.22,
        remaining_income=48877.78,
        risk_level="LOW",
        risk_reasons=["Applicant passes basic financial rules"],
    )

    decision = SimpleNamespace(
        decision="APPROVE",
        reason="Applicant has low credit risk.",
    )

    calls = []

    def fake_assessment_tool(profile):
        calls.append("assessment")
        return assessment

    def fake_prediction_tool(profile):
        calls.append("prediction")
        return 0.03

    def fake_explanation_tool(profile):
        calls.append("explanation")
        return [
            {
                "feature": "credit_score",
                "contribution": -0.5,
                "direction": "lower_risk",
            }
        ]

    def fake_decision_tool(profile, default_probability):
        calls.append("decision")
        assert default_probability == 0.03
        return decision

    def fake_policy_tool(
        foir,
        credit_score,
        previous_defaults,
        default_probability,
        lending_decision,
    ):
        calls.append("policy")

        assert foir == 25.0
        assert credit_score == 780
        assert previous_defaults == 0
        assert default_probability == 0.03
        assert lending_decision == "APPROVE"

        return "FOIR policy guidance."

    monkeypatch.setattr(
        agent_module,
        "credit_assessment_tool",
        fake_assessment_tool,
    )

    monkeypatch.setattr(
        agent_module,
        "ml_prediction_tool",
        fake_prediction_tool,
    )

    monkeypatch.setattr(
        agent_module,
        "ml_explanation_tool",
        fake_explanation_tool,
    )

    monkeypatch.setattr(
        agent_module,
        "lending_decision_tool",
        fake_decision_tool,
    )

    monkeypatch.setattr(
        agent_module,
        "policy_retrieval_tool",
        fake_policy_tool,
    )

    agent = CreditAnalystAgent(
        analyst=fake_analyst,
    )

    result = agent.analyze(
        CreditAnalystAgentInput(
            profile=create_profile()
        )
    )

    assert calls == [
        "assessment",
        "prediction",
        "explanation",
        "decision",
        "policy",
    ]

    assert result.assessment == assessment
    assert result.default_probability == 0.03
    assert result.ml_explanation[0]["feature"] == "credit_score"
    assert result.policy_context == "FOIR policy guidance."
    assert result.lending_decision == decision
    assert result.analyst_explanation == (
        "Mock credit analyst explanation."
    )


def test_agent_passes_grounded_information_to_llm(monkeypatch):

    import app.agents.credit_analyst_agent as agent_module

    fake_analyst = FakeAnalyst()

    assessment = SimpleNamespace(
        foir=25.0,
        emi=11122.22,
        total_obligations=31122.22,
        remaining_income=48877.78,
        risk_level="LOW",
        risk_reasons=["Applicant passes basic financial rules"],
    )

    decision = SimpleNamespace(
        decision="APPROVE",
        reason="Applicant has low credit risk.",
    )

    monkeypatch.setattr(
        agent_module,
        "credit_assessment_tool",
        lambda profile: assessment,
    )

    monkeypatch.setattr(
        agent_module,
        "ml_prediction_tool",
        lambda profile: 0.03,
    )

    monkeypatch.setattr(
        agent_module,
        "ml_explanation_tool",
        lambda profile: [
            {
                "feature": "credit_score",
                "contribution": -0.5,
                "direction": "lower_risk",
            }
        ],
    )

    monkeypatch.setattr(
        agent_module,
        "lending_decision_tool",
        lambda profile, default_probability: decision,
    )

    monkeypatch.setattr(
        agent_module,
        "policy_retrieval_tool",
        lambda **kwargs: "FOIR policy guidance.",
    )

    agent = CreditAnalystAgent(
        analyst=fake_analyst,
    )

    agent.analyze(
        CreditAnalystAgentInput(
            profile=create_profile()
        )
    )

    assert fake_analyst.received is not None
    assert fake_analyst.received.foir == 25.0
    assert fake_analyst.received.default_probability == 0.03
    assert fake_analyst.received.lending_decision == "APPROVE"
    assert fake_analyst.received.policy_context == (
        "FOIR policy guidance."
    )