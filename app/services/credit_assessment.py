from app.finance import (
    FinancialProfile,
    calculate_foir,
    calculate_emi,
    calculate_affordability,
)
from app.services.underwriting import classify_risk
from app.services.decision import CreditDecision


def assess_credit(profile: FinancialProfile):

    profile.validate()

    foir = calculate_foir(
        profile.monthly_income,
        profile.existing_obligations,
    )

    emi = calculate_emi(
        profile.loan_amount,
        profile.annual_interest_rate,
        profile.tenure_years,
    )

    affordability = calculate_affordability(
        monthly_income=profile.monthly_income,
        existing_obligations=profile.existing_obligations,
        proposed_emi=emi,
    )
    risk = classify_risk(
        foir=foir,
        remaining_income=affordability["remaining_income"],
        monthly_income=profile.monthly_income,
    )

    return CreditDecision(
        foir=foir,
        emi=emi,
        total_obligations=affordability["total_obligations"],
        remaining_income=affordability["remaining_income"],
        risk_level=risk["risk_level"],
        risk_reasons=risk["reasons"],
    )