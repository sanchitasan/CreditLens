from app.finance.profile import FinancialProfile
from app.tools.ml_prediction_tool import ml_prediction_tool


def test_ml_prediction_tool_returns_probability():

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

    probability = ml_prediction_tool(profile)

    assert 0.0 <= probability <= 1.0


def test_ml_prediction_tool_returns_lower_risk_for_stronger_profile():

    strong_profile = FinancialProfile(
        monthly_income=80000,
        existing_obligations=20000,
        loan_amount=500000,
        annual_interest_rate=12,
        tenure_years=5,
        credit_score=780,
        employment_years=5,
        previous_defaults=0,
    )

    weak_profile = FinancialProfile(
        monthly_income=50000,
        existing_obligations=29000,
        loan_amount=500000,
        annual_interest_rate=15,
        tenure_years=5,
        credit_score=680,
        employment_years=2,
        previous_defaults=2,
    )

    strong_probability = ml_prediction_tool(strong_profile)
    weak_probability = ml_prediction_tool(weak_profile)

    assert strong_probability < weak_probability