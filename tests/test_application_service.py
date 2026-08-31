from app.finance.profile import FinancialProfile

from app.services.application_service import (
    process_credit_application,
)


def test_process_credit_application():

    profile = FinancialProfile(
        monthly_income=80000,
        existing_obligations=20000,
        loan_amount=500000,
        annual_interest_rate=12,
        tenure_years=5,
    )

    (
        application_id,
        assessment,
        lending_decision,
    ) = process_credit_application(profile)

    assert application_id > 0

    assert assessment.foir == 25.0

    assert round(assessment.emi, 2) == 11122.22

    assert assessment.total_obligations > 0

    assert assessment.remaining_income > 0

    assert assessment.risk_level == "LOW"

    assert lending_decision.decision == "APPROVE"

    assert (
        lending_decision.reason
        == "Applicant has low credit risk."
    )