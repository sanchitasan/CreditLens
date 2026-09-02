from app.finance.profile import FinancialProfile
from app.ml.inference import predict_default_probability


def ml_prediction_tool(
    profile: FinancialProfile,
) -> float:
    """
    Predict the applicant's probability of default
    using the existing trained ML inference pipeline.

    This tool provides an ML risk signal.
    It does not make the lending decision.
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

    return predict_default_probability(features)