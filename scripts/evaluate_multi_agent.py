from app.agents.final_credit_analyst_agent import (
    FinalCreditAnalystAgent,
)
from app.agents.financial_analyst_agent import (
    FinancialAnalystAgent,
)
from app.agents.orchestrator import CreditLensOrchestrator
from app.agents.policy_analyst_agent import (
    PolicyAnalystAgent,
)
from app.agents.risk_analyst_agent import (
    RiskAnalystAgent,
)
from app.finance.profile import FinancialProfile
from app.llm.credit_analyst import CreditAnalyst
from app.llm.gemini_client import GeminiClient


def main():
    profile = FinancialProfile(
        monthly_income=80000,
        existing_obligations=20000,
        loan_amount=500000,
        annual_interest_rate=12,
        tenure_years=5,
        credit_score=780,
        employment_years=5,
        previous_defaults=0,
    )

    gemini_client = GeminiClient()

    final_analyst = FinalCreditAnalystAgent(
        analyst=CreditAnalyst(
            llm_client=gemini_client
        )
    )

    orchestrator = CreditLensOrchestrator(
        financial_agent=FinancialAnalystAgent(),
        risk_agent=RiskAnalystAgent(),
        policy_agent=PolicyAnalystAgent(),
        final_analyst_agent=final_analyst,
    )

    result = orchestrator.assess(profile)

    financial = result.financial_analysis
    risk = result.risk_analysis
    decision = result.lending_decision

    print("\n===== CREDITLENS MULTI-AGENT ASSESSMENT =====")

    print("\n--- Financial Analysis ---")
    print(f"FOIR: {financial.foir:.2f}%")
    print(f"EMI: ₹{financial.emi:.2f}")
    print(
        f"Total Obligations: "
        f"₹{financial.total_obligations:.2f}"
    )
    print(
        f"Remaining Income: "
        f"₹{financial.remaining_income:.2f}"
    )
    print(f"Risk Level: {financial.risk_level}")

    print("\n--- Risk Analysis ---")
    print(
        f"Default Probability: "
        f"{risk.default_probability:.4f}"
    )

    print("\nML Explanation:")
    for item in risk.ml_explanation:
        print(item)

    print("\n--- Lending Decision ---")
    print(f"Decision: {decision.decision}")
    print(f"Reason: {decision.reason}")

    print("\n--- Policy Context ---")
    print(result.policy_analysis.policy_context)

    print("\n--- FINAL CREDIT ANALYST ---")
    print(result.analyst_explanation)


if __name__ == "__main__":
    main()