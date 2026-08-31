from app.finance import FinancialProfile
from app.services.credit_assessment import assess_credit


def test_credit_assessment():

    profile = FinancialProfile(
        monthly_income=80000,
        existing_obligations=20000,
        loan_amount=500000,
        annual_interest_rate=12,
        tenure_years=5,
    )

    result = assess_credit(profile)

    assert result.foir == 25.0
    assert round(result.emi, 2) == 11122.22
    assert result.total_obligations > 0
    assert result.remaining_income > 0
    assert result.risk_level == "LOW"
    assert len(result.risk_reasons) > 0