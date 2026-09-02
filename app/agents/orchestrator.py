from app.agents.assessment_package import CreditAssessmentPackage
from app.agents.financial_analyst_agent import (
    FinancialAnalystAgent,
    FinancialAnalystInput,
)
from app.agents.final_credit_analyst_agent import (
    FinalCreditAnalystAgent,
    FinalCreditAnalystInput,
)
from app.agents.policy_analyst_agent import (
    PolicyAnalystAgent,
    PolicyAnalystInput,
)
from app.agents.risk_analyst_agent import (
    RiskAnalystAgent,
    RiskAnalystInput,
)
from app.finance.profile import FinancialProfile
from app.tools.lending_decision_tool import lending_decision_tool


class CreditLensOrchestrator:
    """
    Coordinates the specialized CreditLens agents.

    The orchestrator does not implement financial,
    ML, or policy rules.
    """

    def __init__(
        self,
        financial_agent: FinancialAnalystAgent,
        risk_agent: RiskAnalystAgent,
        policy_agent: PolicyAnalystAgent,
        final_analyst_agent: FinalCreditAnalystAgent,
    ):
        self.financial_agent = financial_agent
        self.risk_agent = risk_agent
        self.policy_agent = policy_agent
        self.final_analyst_agent = final_analyst_agent

    def assess(
        self,
        profile: FinancialProfile,
    ) -> CreditAssessmentPackage:

        financial_analysis = self.financial_agent.analyze(
            FinancialAnalystInput(profile=profile)
        )

        risk_analysis = self.risk_agent.analyze(
            RiskAnalystInput(profile=profile)
        )

        lending_decision = lending_decision_tool(
            profile=profile,
            default_probability=risk_analysis.default_probability,
        )

        policy_analysis = self.policy_agent.analyze(
            PolicyAnalystInput(
                foir=financial_analysis.foir,
                credit_score=profile.credit_score,
                previous_defaults=profile.previous_defaults,
                default_probability=risk_analysis.default_probability,
                lending_decision=lending_decision.decision,
            )
        )

        package = CreditAssessmentPackage(
            financial_analysis=financial_analysis,
            risk_analysis=risk_analysis,
            policy_analysis=policy_analysis,
            lending_decision=lending_decision,
            rule_risk_level=financial_analysis.risk_level,
            final_risk_level=lending_decision.risk_level,


        )

        final_analysis = self.final_analyst_agent.analyze(
            FinalCreditAnalystInput(
                profile=profile,
                assessment_package=package,
            )
        )

        package.analyst_explanation = (
            final_analysis.analyst_explanation
        )

        return package