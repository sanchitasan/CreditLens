from app.agents.assessment_package import CreditAssessmentPackage
from app.finance.profile import FinancialProfile
from app.audit.decision_trace import DecisionTrace


def build_decision_trace(
    profile: FinancialProfile,
    package: CreditAssessmentPackage,
) -> DecisionTrace:
    """
    Build an audit trace from an existing CreditLens assessment.

    This function does not perform calculations or make decisions.
    It only records the evidence and outputs already produced.
    """

    applicant_data = {
        "monthly_income": profile.monthly_income,
        "existing_obligations": profile.existing_obligations,
        "loan_amount": profile.loan_amount,
        "annual_interest_rate": profile.annual_interest_rate,
        "tenure_years": profile.tenure_years,
        "credit_score": profile.credit_score,
        "employment_years": profile.employment_years,
        "previous_defaults": profile.previous_defaults,
    }

    return DecisionTrace(
        applicant_data=applicant_data,
        financial_analysis=package.financial_analysis,
        risk_analysis=package.risk_analysis,
        policy_context=(
            package.policy_analysis.policy_context
        ),
        rule_risk_level=package.rule_risk_level,
        final_risk_level=package.final_risk_level,
        lending_decision=package.lending_decision,
        analyst_explanation=package.analyst_explanation,
    )