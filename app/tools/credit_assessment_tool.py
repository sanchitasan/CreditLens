from app.finance.profile import FinancialProfile
from app.services.credit_assessment import assess_credit


def credit_assessment_tool(
    profile: FinancialProfile,
):
    """
    Run the existing deterministic credit assessment
    for a financial profile.

    This tool does not make the final lending decision.
    """

    profile.validate()

    return assess_credit(profile)