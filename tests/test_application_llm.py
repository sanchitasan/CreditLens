from app.finance.profile import FinancialProfile
from app.services.application_service import process_credit_application


class FakeCreditAnalyst:
    """
    Fake Credit Analyst used for testing.

    No Gemini API call is made.
    """

    def analyze(self, application):
        return "Applicant has low default risk and the lending decision is APPROVE."


def test_application_service_uses_credit_analyst(monkeypatch):

    monkeypatch.setattr(
        "app.services.application_service.CreditAnalyst",
        lambda *args, **kwargs: FakeCreditAnalyst(),
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

    assert assessment.analyst_explanation == (
        "Applicant has low default risk and the lending decision is APPROVE."
    )