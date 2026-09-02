from types import SimpleNamespace

import app.agents.credit_analyst_agent as agent_module
from app.agents.credit_analyst_agent import (
    CreditAnalystAgent,
    CreditAnalystAgentInput,
)
from app.finance.profile import FinancialProfile


class FakeAnalyst:

    def __init__(self):
        self.received = []

    def analyze(self, application):

        self.received.append(application)

        return (
            f"Decision: {application.lending_decision}. "
            f"Policy context supplied: "
            f"{bool(application.policy_context)}"
        )


def strong_profile():
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


def weak_profile():
    return FinancialProfile(
        monthly_income=50000,
        existing_obligations=29000,
        loan_amount=500000,
        annual_interest_rate=15,
        tenure_years=5,
        credit_score=680,
        employment_years=2,
        previous_defaults=2,
    )


def configure_fake_tools(monkeypatch):

    def fake_assessment(profile):

        if profile.credit_score >= 750:
            return SimpleNamespace(
                foir=25.0,
                emi=11122.22,
                total_obligations=31122.22,
                remaining_income=48877.78,
                risk_level="LOW",
                risk_reasons=[
                    "Applicant passes basic financial rules"
                ],
            )

        return SimpleNamespace(
            foir=58.0,
            emi=11894.97,
            total_obligations=40894.97,
            remaining_income=9105.03,
            risk_level="HIGH",
            risk_reasons=[
                "FOIR exceeds critical threshold"
            ],
        )

    def fake_prediction(profile):

        if profile.credit_score >= 750:
            return 0.03

        return 0.28

    def fake_explanation(profile):

        return [
            {
                "feature": "credit_score",
                "contribution": -3.9,
                "direction": "reduces default risk",
            }
        ]

    def fake_decision(profile, default_probability):

        if profile.credit_score >= 750:
            return SimpleNamespace(
                decision="APPROVE",
                reason="Applicant has low credit risk.",
            )

        return SimpleNamespace(
            decision="REJECT",
            reason="Applicant has high credit risk.",
        )

    def fake_policy(**kwargs):

        return (
            "[Policy Context 1]\n"
            "FOIR Guidelines\n\n"
            "[Policy Context 2]\n"
            "Credit Score Guidelines\n\n"
            "[Policy Context 3]\n"
            "Previous Defaults\n\n"
            "[Policy Context 4]\n"
            "ML Default Probability\n\n"
            "[Policy Context 5]\n"
            "Lending Decisions"
        )

    monkeypatch.setattr(
        agent_module,
        "credit_assessment_tool",
        fake_assessment,
    )

    monkeypatch.setattr(
        agent_module,
        "ml_prediction_tool",
        fake_prediction,
    )

    monkeypatch.setattr(
        agent_module,
        "ml_explanation_tool",
        fake_explanation,
    )

    monkeypatch.setattr(
        agent_module,
        "lending_decision_tool",
        fake_decision,
    )

    monkeypatch.setattr(
        agent_module,
        "policy_retrieval_tool",
        fake_policy,
    )


def test_strong_applicant_is_approved(monkeypatch):

    configure_fake_tools(monkeypatch)

    analyst = FakeAnalyst()

    agent = CreditAnalystAgent(
        analyst=analyst
    )

    result = agent.analyze(
        CreditAnalystAgentInput(
            profile=strong_profile()
        )
    )

    assert result.assessment.risk_level == "LOW"
    assert result.default_probability == 0.03
    assert result.lending_decision.decision == "APPROVE"

    assert result.policy_context.count(
        "[Policy Context"
    ) == 5

    assert len(analyst.received) == 1

    llm_input = analyst.received[0]

    assert llm_input.lending_decision == "APPROVE"
    assert llm_input.default_probability == 0.03
    assert llm_input.policy_context


def test_weak_applicant_is_rejected(monkeypatch):

    configure_fake_tools(monkeypatch)

    analyst = FakeAnalyst()

    agent = CreditAnalystAgent(
        analyst=analyst
    )

    result = agent.analyze(
        CreditAnalystAgentInput(
            profile=weak_profile()
        )
    )

    assert result.assessment.risk_level == "HIGH"
    assert result.default_probability == 0.28
    assert result.lending_decision.decision == "REJECT"

    assert result.policy_context.count(
        "[Policy Context"
    ) == 5

    llm_input = analyst.received[0]

    assert llm_input.lending_decision == "REJECT"
    assert llm_input.default_probability == 0.28
    assert llm_input.policy_context