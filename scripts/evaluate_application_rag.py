from app.finance.profile import FinancialProfile
from app.services.application_service import process_credit_application


class CapturingCreditAnalyst:

    captured_inputs = []

    def __init__(self, *args, **kwargs):
        pass

    def analyze(self, application):
        self.captured_inputs.append(application)
        return "Captured for RAG evaluation."


def evaluate_application(name, profile):

    CapturingCreditAnalyst.captured_inputs = []

    import app.services.application_service as application_service

    original_analyst = application_service.CreditAnalyst
    application_service.CreditAnalyst = CapturingCreditAnalyst

    try:
        (
            application_id,
            assessment,
            lending_decision,
        ) = process_credit_application(profile)

        analyst_input = CapturingCreditAnalyst.captured_inputs[0]

        print("\n" + "=" * 70)
        print(name)
        print("=" * 70)

        print("\nAPPLICATION")
        print("Monthly income:", profile.monthly_income)
        print("Existing obligations:", profile.existing_obligations)
        print("Loan amount:", profile.loan_amount)
        print("Credit score:", profile.credit_score)
        print("Previous defaults:", profile.previous_defaults)

        print("\nASSESSMENT")
        print("FOIR:", assessment.foir)
        print("EMI:", assessment.emi)
        print("Risk level:", assessment.risk_level)
        print("Default probability:", assessment.default_probability)

        print("\nLENDING DECISION")
        print("Decision:", lending_decision.decision)
        print("Reason:", lending_decision.reason)

        print("\nPOLICY CONTEXT SENT TO CREDIT ANALYST")
        print("-" * 70)
        print(analyst_input.policy_context)

        print("-" * 70)

        return {
            "application_id": application_id,
            "assessment": assessment,
            "decision": lending_decision,
            "policy_context": analyst_input.policy_context,
        }

    finally:
        application_service.CreditAnalyst = original_analyst


def main():

    low_risk_profile = FinancialProfile(
        monthly_income=80000,
        existing_obligations=20000,
        loan_amount=500000,
        annual_interest_rate=12,
        tenure_years=5,
        credit_score=780,
        employment_years=5,
        previous_defaults=0,
    )

    high_risk_profile = FinancialProfile(
        monthly_income=50000,
        existing_obligations=29000,
        loan_amount=500000,
        annual_interest_rate=15,
        tenure_years=5,
        credit_score=680,
        employment_years=2,
        previous_defaults=2,
    )

    evaluate_application(
        "Low-risk application",
        low_risk_profile,
    )

    evaluate_application(
        "High-risk application",
        high_risk_profile,
    )


if __name__ == "__main__":
    main()