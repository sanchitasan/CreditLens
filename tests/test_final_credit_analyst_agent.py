from types import SimpleNamespace

from app.agents.assessment_package import CreditAssessmentPackage
from app.agents.final_credit_analyst_agent import (
    FinalCreditAnalystAgent,
    FinalCreditAnalystInput,
)
from app.finance.profile import FinancialProfile


class FakeAnalyst:
    def __init__(self):
        self.received_input = None

    def analyze(self, analyst_input):
        self.received_input = analyst_input
        return "Final credit assessment generated."


def build_profile():
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


def build_package():
    financial_analysis = SimpleNamespace(
        foir=25.0,
        emi=11122.22,
        total_obligations=31122.22,
        remaining_income=48877.78,
        risk_level="LOW",
        risk_reasons=[
            "Applicant passes basic financial rules"
        ],
    )

    risk_analysis = SimpleNamespace(
        default_probability=0.03,
        ml_explanation=[
            {
                "feature": "credit_score",
                "direction": "reduces risk",
                "contribution": -3.93,
            }
        ],
    )

    policy_analysis = SimpleNamespace(
        policy_context="Retrieved policy context."
    )

    lending_decision = SimpleNamespace(
        decision="APPROVE",
        reason="Applicant has low credit risk.",
    )

    return CreditAssessmentPackage(
        financial_analysis=financial_analysis,
        risk_analysis=risk_analysis,
        policy_analysis=policy_analysis,
        lending_decision=lending_decision,
    )


def test_final_credit_analyst_generates_explanation():
    fake_analyst = FakeAnalyst()

    agent = FinalCreditAnalystAgent(
        analyst=fake_analyst
    )

    profile = build_profile()
    package = build_package()

    result = agent.analyze(
        FinalCreditAnalystInput(
            profile=profile,
            assessment_package=package,
        )
    )

    assert result.analyst_explanation == (
        "Final credit assessment generated."
    )


def test_final_credit_analyst_receives_complete_evidence():
    fake_analyst = FakeAnalyst()

    agent = FinalCreditAnalystAgent(
        analyst=fake_analyst
    )

    profile = build_profile()
    package = build_package()

    agent.analyze(
        FinalCreditAnalystInput(
            profile=profile,
            assessment_package=package,
        )
    )

    received = fake_analyst.received_input

    assert received.monthly_income == 80000
    assert received.existing_obligations == 20000
    assert received.loan_amount == 500000

    assert received.foir == 25.0
    assert received.emi == 11122.22
    assert received.remaining_income == 48877.78

    assert received.default_probability == 0.03
    assert received.ml_explanation[0]["feature"] == "credit_score"

    assert received.lending_decision == "APPROVE"
    assert received.decision_reason == (
        "Applicant has low credit risk."
    )

    assert received.policy_context == (
        "Retrieved policy context."
    )


def test_final_credit_analyst_does_not_change_decision():
    fake_analyst = FakeAnalyst()

    agent = FinalCreditAnalystAgent(
        analyst=fake_analyst
    )

    profile = build_profile()
    package = build_package()

    result = agent.analyze(
        FinalCreditAnalystInput(
            profile=profile,
            assessment_package=package,
        )
    )

    assert package.lending_decision.decision == "APPROVE"
    assert result.analyst_explanation == (
        "Final credit assessment generated."
    )