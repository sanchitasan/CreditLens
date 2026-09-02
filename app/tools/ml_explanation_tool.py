from app.finance.profile import FinancialProfile
from app.ml.inference import explain_default_prediction
from app.ml.explanation import explain_prediction


def ml_explanation_tool(
    profile: FinancialProfile,
    top_n: int = 3,
) -> list[dict]:
    """
    Explain the ML default prediction using feature-level
    contributions.

    This tool explains the ML signal.
    It does not make or change the lending decision.
    """

    profile.validate()

    features = [
        profile.monthly_income,
        profile.existing_obligations,
        profile.loan_amount,
        profile.annual_interest_rate,
        profile.tenure_years,
        profile.credit_score,
        profile.employment_years,
        profile.previous_defaults,
    ]

    contributions = explain_default_prediction(features)

    return explain_prediction(
        contributions,
        top_n=top_n,
    )