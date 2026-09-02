from dataclasses import dataclass

from app.finance.profile import FinancialProfile
from app.tools.ml_explanation_tool import ml_explanation_tool
from app.tools.ml_prediction_tool import ml_prediction_tool


@dataclass
class RiskAnalysis:
    """ML-based risk analysis produced by the Risk Analyst Agent."""

    default_probability: float
    ml_explanation: list[dict]


@dataclass
class RiskAnalystInput:
    """Input provided to the Risk Analyst Agent."""

    profile: FinancialProfile


class RiskAnalystAgent:
    """
    Specialized agent responsible for ML-based risk analysis.

    It uses the existing ML prediction and explanation tools.
    It does not make or override the lending decision.
    """

    def analyze(
        self,
        agent_input: RiskAnalystInput,
    ) -> RiskAnalysis:

        profile = agent_input.profile

        default_probability = ml_prediction_tool(
            profile
        )

        ml_explanation = ml_explanation_tool(
            profile
        )

        return RiskAnalysis(
            default_probability=default_probability,
            ml_explanation=ml_explanation,
        )