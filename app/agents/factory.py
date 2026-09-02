from app.agents.financial_analyst_agent import (
    FinancialAnalystAgent,
)
from app.agents.final_credit_analyst_agent import (
    FinalCreditAnalystAgent,
)
from app.agents.orchestrator import (
    CreditLensOrchestrator,
)
from app.agents.policy_analyst_agent import (
    PolicyAnalystAgent,
)
from app.agents.risk_analyst_agent import (
    RiskAnalystAgent,
)
from app.llm.credit_analyst import (
    CreditAnalyst,
)
from app.llm.gemini_client import (
    GeminiClient,
)


def create_creditlens_orchestrator():
    analyst = CreditAnalyst(
        GeminiClient()
    )

    financial_agent = FinancialAnalystAgent()

    risk_agent = RiskAnalystAgent()

    policy_agent = PolicyAnalystAgent()

    final_analyst_agent = FinalCreditAnalystAgent(
        analyst=analyst
    )

    return CreditLensOrchestrator(
        financial_agent=financial_agent,
        risk_agent=risk_agent,
        policy_agent=policy_agent,
        final_analyst_agent=final_analyst_agent,
    )