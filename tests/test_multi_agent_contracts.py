from app.agents.assessment_package import CreditAssessmentPackage
from app.agents.financial_analyst_agent import (
    FinancialAnalysis,
    FinancialAnalystInput,
)
from app.agents.policy_analyst_agent import (
    PolicyAnalysis,
    PolicyAnalystInput,
)
from app.agents.risk_analyst_agent import (
    RiskAnalysis,
    RiskAnalystInput,
)
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


def test_financial_analysis_contract():

    result = FinancialAnalysis(
        foir=25.0,
        emi=11122.22,
        total_obligations=31122.22,
        remaining_income=48877.78,
        risk_level="LOW",
        risk_reasons=[
            "Applicant passes basic financial rules"
        ],
    )

    assert result.foir == 25.0
    assert result.emi > 0
    assert result.total_obligations > 0
    assert result.remaining_income > 0
    assert result.risk_level == "LOW"
    assert isinstance(result.risk_reasons, list)


def test_financial_analyst_input_contract():

    profile = create_profile()

    result = FinancialAnalystInput(
        profile=profile
    )

    assert result.profile == profile


def test_risk_analysis_contract():

    result = RiskAnalysis(
        default_probability=0.03,
        ml_explanation=[
            {
                "feature": "credit_score",
                "contribution": -3.9,
                "direction": "reduces default risk",
            }
        ],
    )

    assert 0 <= result.default_probability <= 1
    assert isinstance(result.ml_explanation, list)


def test_risk_analyst_input_contract():

    profile = create_profile()

    result = RiskAnalystInput(
        profile=profile
    )

    assert result.profile == profile


def test_policy_analysis_contract():

    result = PolicyAnalysis(
        policy_context="FOIR policy guidance."
    )

    assert isinstance(result.policy_context, str)
    assert result.policy_context


def test_policy_analyst_input_contract():

    result = PolicyAnalystInput(
        foir=25.0,
        credit_score=780,
        previous_defaults=0,
        default_probability=0.03,
        lending_decision="APPROVE",
    )

    assert result.foir == 25.0
    assert result.credit_score == 780
    assert result.previous_defaults == 0
    assert result.default_probability == 0.03
    assert result.lending_decision == "APPROVE"


def test_credit_assessment_package_contract():

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
        ml_explanation=[],
    )

    policy = PolicyAnalysis(
        policy_context="FOIR policy guidance."
    )

    decision = {
        "decision": "APPROVE",
        "reason": "Applicant has low credit risk.",
    }

    package = CreditAssessmentPackage(
        financial_analysis=financial,
        risk_analysis=risk,
        policy_analysis=policy,
        lending_decision=decision,
    )

    assert package.financial_analysis == financial
    assert package.risk_analysis == risk
    assert package.policy_analysis == policy
    assert package.lending_decision == decision