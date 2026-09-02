from dataclasses import dataclass

from app.finance.profile import FinancialProfile
from app.tools.credit_assessment_tool import credit_assessment_tool


@dataclass
class FinancialAnalysis:
    """Financial assessment produced by the Financial Analyst Agent."""

    foir: float
    emi: float
    total_obligations: float
    remaining_income: float
    risk_level: str
    risk_reasons: list[str]


@dataclass
class FinancialAnalystInput:
    """Input provided to the Financial Analyst Agent."""

    profile: FinancialProfile


class FinancialAnalystAgent:
    """
    Specialized agent responsible for financial assessment.

    All financial calculations and deterministic financial
    rules remain inside the existing tested tool layer.
    """

    def analyze(
        self,
        agent_input: FinancialAnalystInput,
    ) -> FinancialAnalysis:

        assessment = credit_assessment_tool(
            agent_input.profile
        )

        return FinancialAnalysis(
            foir=assessment.foir,
            emi=assessment.emi,
            total_obligations=assessment.total_obligations,
            remaining_income=assessment.remaining_income,
            risk_level=assessment.risk_level,
            risk_reasons=assessment.risk_reasons,
        )