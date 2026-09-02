from app.finance.profile import FinancialProfile
from app.services.credit_assessment import assess_credit
from app.services.underwriting import combine_risk_assessment
from app.services.decision import make_credit_decision


def lending_decision_tool(
    profile: FinancialProfile,
    default_probability: float,
):
    """
    Generate the authoritative lending decision using the
    existing deterministic underwriting and decision logic.

    The ML default probability is used as a risk signal.
    This tool does not use an LLM and does not independently
    make lending rules.
    """

    profile.validate()

    assessment = assess_credit(profile)

    final_risk_level = combine_risk_assessment(
        rule_risk_level=assessment.risk_level,
        default_probability=default_probability,
    )

    return make_credit_decision(
        risk_level=final_risk_level,
        default_probability=default_probability,
    )