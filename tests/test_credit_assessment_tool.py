import pytest

from app.finance.profile import FinancialProfile
from app.tools.credit_assessment_tool import credit_assessment_tool


def test_credit_assessment_tool_returns_assessment():

    profile = FinancialProfile(
        monthly_income=80000,
        existing_obligations=20000,
        loan_amount=500000,
        annual_interest_rate=12,
        tenure_years=5,
    )

    assessment = credit_assessment_tool(profile)

    assert assessment.foir == 25.0
    assert round(assessment.emi, 2) == 11122.22
    assert assessment.total_obligations > 0
    assert assessment.remaining_income > 0
    assert assessment.risk_level == "LOW"


def test_credit_assessment_tool_validates_profile():

    profile = FinancialProfile(
        monthly_income=-1000,
        existing_obligations=20000,
        loan_amount=500000,
        annual_interest_rate=12,
        tenure_years=5,
    )

    with pytest.raises(ValueError):
        credit_assessment_tool(profile)