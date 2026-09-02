from app.finance.profile import FinancialProfile
from app.tools.ml_explanation_tool import ml_explanation_tool


def test_ml_explanation_tool_returns_feature_explanations():

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

    explanation = ml_explanation_tool(profile)

    assert isinstance(explanation, list)
    assert len(explanation) > 0

    for item in explanation:
        assert "feature" in item
        assert "contribution" in item
        assert "direction" in item


def test_ml_explanation_tool_respects_top_n():

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

    explanation = ml_explanation_tool(
        profile,
        top_n=2,
    )

    assert len(explanation) <= 2