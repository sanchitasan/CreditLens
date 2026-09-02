from dataclasses import dataclass

from app.finance.profile import FinancialProfile
from app.llm.credit_analyst import CreditAnalyst, CreditAnalystInput
from app.tools.credit_assessment_tool import credit_assessment_tool
from app.tools.lending_decision_tool import lending_decision_tool
from app.tools.ml_explanation_tool import ml_explanation_tool
from app.tools.ml_prediction_tool import ml_prediction_tool
from app.tools.policy_retrieval_tool import policy_retrieval_tool


@dataclass
class CreditAnalystAgentInput:
    """Input provided to the Credit Analyst Agent."""

    profile: FinancialProfile


@dataclass
class CreditAnalystAgentOutput:
    """Auditable output produced by the Credit Analyst Agent."""

    assessment: object
    default_probability: float
    ml_explanation: list[dict]
    policy_context: str
    lending_decision: object
    analyst_explanation: str


class CreditAnalystAgent:
    """
    Single-agent orchestration layer for CreditLens.

    The agent coordinates existing deterministic tools
    and passes their results to the LLM Credit Analyst.

    The agent does not implement lending rules itself.
    """

    def __init__(self, analyst: CreditAnalyst):
        self.analyst = analyst

    def analyze(
        self,
        agent_input: CreditAnalystAgentInput,
    ) -> CreditAnalystAgentOutput:

        profile = agent_input.profile

        # -------------------------------------------------
        # 1. Deterministic credit assessment
        # -------------------------------------------------

        assessment = credit_assessment_tool(profile)

        # -------------------------------------------------
        # 2. ML default probability
        # -------------------------------------------------

        default_probability = ml_prediction_tool(profile)

        # -------------------------------------------------
        # 3. ML explanation
        # -------------------------------------------------

        ml_explanation = ml_explanation_tool(profile)

        # -------------------------------------------------
        # 4. Authoritative lending decision
        # -------------------------------------------------

        lending_decision = lending_decision_tool(
            profile=profile,
            default_probability=default_probability,
        )

        # -------------------------------------------------
        # 5. Retrieve policy using the actual decision
        # -------------------------------------------------

        policy_context = policy_retrieval_tool(
            foir=assessment.foir,
            credit_score=profile.credit_score,
            previous_defaults=profile.previous_defaults,
            default_probability=default_probability,
            lending_decision=lending_decision.decision,
        )

        # -------------------------------------------------
        # 6. Build grounded LLM input
        # -------------------------------------------------

        analyst_input = CreditAnalystInput(
            monthly_income=profile.monthly_income,
            existing_obligations=profile.existing_obligations,
            loan_amount=profile.loan_amount,
            annual_interest_rate=profile.annual_interest_rate,
            tenure_years=profile.tenure_years,
            credit_score=profile.credit_score,
            employment_years=profile.employment_years,
            previous_defaults=profile.previous_defaults,
            foir=assessment.foir,
            emi=assessment.emi,
            total_obligations=assessment.total_obligations,
            remaining_income=assessment.remaining_income,
            risk_level=assessment.risk_level,
            default_probability=default_probability,
            ml_explanation=ml_explanation,
            lending_decision=lending_decision.decision,
            decision_reason=lending_decision.reason,
            policy_context=policy_context,
        )

        # -------------------------------------------------
        # 7. Generate analyst explanation
        # -------------------------------------------------

        analyst_explanation = self.analyst.analyze(
            analyst_input
        )

        return CreditAnalystAgentOutput(
            assessment=assessment,
            default_probability=default_probability,
            ml_explanation=ml_explanation,
            policy_context=policy_context,
            lending_decision=lending_decision,
            analyst_explanation=analyst_explanation,
        )