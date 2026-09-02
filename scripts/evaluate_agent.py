from app.agents.credit_analyst_agent import (
    CreditAnalystAgent,
    CreditAnalystAgentInput,
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

    llm_client = GeminiClient()

    analyst = CreditAnalyst(
        llm_client=llm_client,
    )

    agent = CreditAnalystAgent(
        analyst=analyst,
    )

    result = agent.analyze(
        CreditAnalystAgentInput(
            profile=profile,
        )
    )

    print("\n" + "=" * 70)
    print("CREDITLENS AGENT RESULT")
    print("=" * 70)

    print("\nFINANCIAL ASSESSMENT")
    print(f"FOIR: {result.assessment.foir:.2f}%")
    print(f"EMI: ₹{result.assessment.emi:,.2f}")
    print(
        f"Remaining income: "
        f"₹{result.assessment.remaining_income:,.2f}"
    )
    print(f"Risk level: {result.assessment.risk_level}")

    print("\nML RISK")
    print(
        f"Default probability: "
        f"{result.default_probability:.4f}"
    )

    print("\nML EXPLANATION")
    for item in result.ml_explanation:
        print(
            f"- {item['feature']}: "
            f"{item['direction']} "
            f"({item['contribution']:.4f})"
        )

    print("\nLENDING DECISION")
    print(f"Decision: {result.lending_decision.decision}")
    print(f"Reason: {result.lending_decision.reason}")

    print("\nPOLICY CONTEXT")
    print(result.policy_context)

    print("\nANALYST EXPLANATION")
    print(result.analyst_explanation)

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()