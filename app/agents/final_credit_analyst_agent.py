from dataclasses import dataclass

from app.agents.assessment_package import CreditAssessmentPackage
from app.finance.profile import FinancialProfile
from app.llm.credit_analyst import CreditAnalyst, CreditAnalystInput


@dataclass
class FinalCreditAnalystInput:
    profile: FinancialProfile
    assessment_package: CreditAssessmentPackage


@dataclass
class FinalCreditAnalystOutput:
    analyst_explanation: str


class FinalCreditAnalystAgent:
    """
    Produces the final human-readable credit assessment.

    This agent does not make or modify the lending decision.
    It explains the evidence and authoritative decision
    already produced by CreditLens.
    """

    def __init__(self, analyst: CreditAnalyst):
        self.analyst = analyst

    def analyze(
        self,
        agent_input: FinalCreditAnalystInput,
    ) -> FinalCreditAnalystOutput:

        profile = agent_input.profile
        package = agent_input.assessment_package

        financial = package.financial_analysis
        risk = package.risk_analysis
        policy = package.policy_analysis
        decision = package.lending_decision

        analyst_input = CreditAnalystInput(
            monthly_income=profile.monthly_income,
            existing_obligations=profile.existing_obligations,
            loan_amount=profile.loan_amount,
            annual_interest_rate=profile.annual_interest_rate,
            tenure_years=profile.tenure_years,
            credit_score=profile.credit_score,
            employment_years=profile.employment_years,
            previous_defaults=profile.previous_defaults,

            foir=financial.foir,
            emi=financial.emi,
            total_obligations=financial.total_obligations,
            remaining_income=financial.remaining_income,
            risk_level=financial.risk_level,

            default_probability=risk.default_probability,
            ml_explanation=risk.ml_explanation,

            lending_decision=decision.decision,
            decision_reason=decision.reason,

            policy_context=policy.policy_context,
        )

        explanation = self.analyst.analyze(analyst_input)

        return FinalCreditAnalystOutput(
            analyst_explanation=explanation,
        )