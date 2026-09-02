from app.finance.profile import FinancialProfile
from app.tools.lending_decision_tool import lending_decision_tool


def test_lending_decision_tool_approves_strong_profile():
    profile = FinancialProfile(
        monthly_income=80000,
        existing_obligations=20000,
        loan_amount=500000,
        annual_interest_rate=12,
        tenure_years=5,
        credit_score=780,
        employment_years=5,
        previous_defaults=0,
    )

    result = lending_decision_tool(
        profile=profile,
        default_probability=0.03,
    )

    assert result.decision == "APPROVE"


def test_lending_decision_tool_rejects_weak_profile():
    profile = FinancialProfile(
        monthly_income=50000,
        existing_obligations=29000,
        loan_amount=500000,
        annual_interest_rate=15,
        tenure_years=5,
        credit_score=680,
        employment_years=2,
        previous_defaults=2,
    )

    result = lending_decision_tool(
        profile=profile,
        default_probability=0.28,
    )

    assert result.decision == "REJECT"