from app.finance.profile import FinancialProfile
from app.services.application_service import process_credit_application


def test_application_service_uses_ml_prediction(monkeypatch):

    monkeypatch.setattr(
        "app.services.application_service.predict_default_probability",
        lambda features: 0.20,
    )

    class FakeCreditAnalyst:

        def __init__(self, *args, **kwargs):
            pass

        def analyze(self, assessment):
            return "Applicant has low credit risk."

    monkeypatch.setattr(
        "app.services.application_service.CreditAnalyst",
        FakeCreditAnalyst,
    )

    profile = FinancialProfile(
        monthly_income=80000,
        existing_obligations=20000,
        loan_amount=500000,
        annual_interest_rate=12,
        tenure_years=5,
        credit_score=750,
        employment_years=4,
        previous_defaults=0,
    )

    application_id, assessment, lending_decision = (
        process_credit_application(profile)
    )

    assert application_id > 0
    assert assessment.default_probability == 0.20