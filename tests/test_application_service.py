from types import SimpleNamespace

from app.finance.profile import FinancialProfile

from app.services.application_service import (
    process_credit_application,
)

import app.services.application_service as application_service_module

from app.agents.financial_analyst_agent import (
    FinancialAnalysis,
)

from app.agents.risk_analyst_agent import (
    RiskAnalysis,
)

from app.agents.policy_analyst_agent import (
    PolicyAnalysis,
)
from app.audit.decision_trace import DecisionTrace

class FakeOrchestrator:

    def assess(self, profile):

        financial_analysis = FinancialAnalysis(
            foir=25.0,
            emi=11122.22,
            total_obligations=31122.22,
            remaining_income=48877.78,
            risk_level="LOW",
            risk_reasons=[
                "Applicant passes basic financial rules"
            ],
        )

        risk_analysis = RiskAnalysis(
            default_probability=0.03,
            ml_explanation=[
                {
                    "feature": "credit_score",
                    "contribution": -3.9,
                    "direction": "reduces default risk",
                }
            ],
        )

        policy_analysis = PolicyAnalysis(
            policy_context="FOIR policy guidance."
        )

        lending_decision = SimpleNamespace(
            decision="APPROVE",
            reason="Applicant has low credit risk.",

        )
        decision_trace = DecisionTrace(
            applicant_data={
                "monthly_income": profile.monthly_income,
                "existing_obligations": profile.existing_obligations,
                "loan_amount": profile.loan_amount,
                "annual_interest_rate": profile.annual_interest_rate,
                "tenure_years": profile.tenure_years,
            },
            financial_analysis=financial_analysis,
            risk_analysis=risk_analysis,
            policy_context=policy_analysis.policy_context,
            rule_risk_level="LOW",
            final_risk_level="LOW",
            lending_decision=lending_decision,
            analyst_explanation=(
                "Applicant has low credit risk."
            ),

        )

        return SimpleNamespace(
            financial_analysis=financial_analysis,
            risk_analysis=risk_analysis,
            policy_analysis=policy_analysis,
            lending_decision=lending_decision,
            rule_risk_level="LOW",
            final_risk_level="LOW",
            analyst_explanation=(
                "Applicant has low credit risk."
            ),
            decision_trace=decision_trace,
        )


def test_process_credit_application(monkeypatch):

    fake_orchestrator = FakeOrchestrator()

    monkeypatch.setattr(
        application_service_module,
        "create_creditlens_orchestrator",
        lambda: fake_orchestrator,
    )

    saved_decision_trace = None

    def fake_save_credit_application(
        profile,
        result,
        lending_decision,
        decision_trace=None,
        connection=None,
    ):
        nonlocal saved_decision_trace

        saved_decision_trace = decision_trace

        return 1

    monkeypatch.setattr(
        application_service_module,
        "save_credit_application",
        fake_save_credit_application,
    )

    profile = FinancialProfile(
        monthly_income=80000,
        existing_obligations=20000,
        loan_amount=500000,
        annual_interest_rate=12,
        tenure_years=5,
    )

    (
        application_id,
        assessment,
        lending_decision,
    ) = process_credit_application(profile)

    assert application_id > 0

    assert assessment.foir == 25.0

    assert round(assessment.emi, 2) == 11122.22

    assert assessment.total_obligations > 0

    assert assessment.remaining_income > 0

    assert assessment.risk_level == "LOW"

    assert assessment.default_probability == 0.03

    assert assessment.analyst_explanation == (
        "Applicant has low credit risk."
    )

    assert lending_decision.decision == "APPROVE"

    assert (
        lending_decision.reason
        == "Applicant has low credit risk."
    )

    assert saved_decision_trace is not None

    assert (
        saved_decision_trace.rule_risk_level
        == "LOW"
    )

    assert (
        saved_decision_trace.final_risk_level
        == "LOW"
    )