from app.audit.trace_builder import build_decision_trace
from app.agents.assessment_package import CreditAssessmentPackage
from app.agents.financial_analyst_agent import FinancialAnalysis
from app.agents.risk_analyst_agent import RiskAnalysis
from app.agents.policy_analyst_agent import PolicyAnalysis
from app.finance.profile import FinancialProfile


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


def create_package():
    financial = FinancialAnalysis(
        foir=25.0,
        emi=11122.22,
        total_obligations=31122.22,
        remaining_income=48877.78,
        risk_level="LOW",
        risk_reasons=[
            "Applicant passes basic financial rules"
        ],
    )

    risk = RiskAnalysis(
        default_probability=0.03,
        ml_explanation=[
            {
                "feature": "credit_score",
                "contribution": -3.9,
                "direction": "reduces default risk",
            }
        ],
    )

    policy = PolicyAnalysis(
        policy_context="FOIR policy guidance."
    )

    decision = {
        "decision": "APPROVE",
        "reason": "Applicant has low credit risk.",
    }

    return CreditAssessmentPackage(
        financial_analysis=financial,
        risk_analysis=risk,
        policy_analysis=policy,
        lending_decision=decision,
        rule_risk_level="LOW",
        final_risk_level="LOW",
        analyst_explanation="Final analyst explanation.",
    )


def test_build_decision_trace():

    profile = create_profile()
    package = create_package()

    trace = build_decision_trace(
        profile=profile,
        package=package,
    )

    assert trace.applicant_data["monthly_income"] == 80000

    assert trace.applicant_data["credit_score"] == 780

    assert trace.financial_analysis == (
        package.financial_analysis
    )

    assert trace.risk_analysis == (
        package.risk_analysis
    )

    assert trace.policy_context == (
        "FOIR policy guidance."
    )

    assert trace.rule_risk_level == "LOW"

    assert trace.final_risk_level == "LOW"

    assert trace.lending_decision == (
        package.lending_decision
    )

    assert trace.analyst_explanation == (
        "Final analyst explanation."
    )