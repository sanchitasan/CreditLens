import pytest

from app.finance import FinancialProfile


def test_valid_financial_profile():

    profile = FinancialProfile(
        monthly_income=80000,
        existing_obligations=20000,
        loan_amount=500000,
        annual_interest_rate=12,
        tenure_years=5
    )

    profile.validate()


def test_negative_income():

    profile = FinancialProfile(
        monthly_income=-80000,
        existing_obligations=20000,
        loan_amount=500000,
        annual_interest_rate=12,
        tenure_years=5
    )

    with pytest.raises(ValueError):
        profile.validate()