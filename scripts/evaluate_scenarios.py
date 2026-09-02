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


SCENARIOS = {
    "LOW_RISK": FinancialProfile(
        monthly_income=80000,
        existing_obligations=20000,
        loan_amount=500000,
        annual_interest_rate=12,
        tenure_years=5,
        credit_score=780,
        employment_years=5,
        previous_defaults=0,
    ),

    "MEDIUM_RISK": FinancialProfile(
        monthly_income=60000,
        existing_obligations=27000,
        loan_amount=300000,
        annual_interest_rate=12,
        tenure_years=5,
        credit_score=700,
        employment_years=3,
        previous_defaults=0,
    ),

    "HIGH_RISK": FinancialProfile(
        monthly_income=50000,
        existing_obligations=29000,
        loan_amount=500000,
        annual_interest_rate=15,
        tenure_years=5,
        credit_score=680,
        employment_years=2,
        previous_defaults=2,
    ),
}


def build_orchestrator():
    gemini_client = GeminiClient()

    final_analyst = FinalCreditAnalystAgent(
        analyst=CreditAnalyst(
            llm_client=gemini_client
        )
    )

    return CreditLensOrchestrator(
        financial_agent=FinancialAnalystAgent(),
        risk_agent=RiskAnalystAgent(),
        policy_agent=PolicyAnalystAgent(),
        final_analyst_agent=final_analyst,
    )


def evaluate_scenario(name, profile):
    orchestrator = build_orchestrator()

    result = orchestrator.assess(profile)

    financial = result.financial_analysis
    risk = result.risk_analysis
    decision = result.lending_decision

    print("\n" + "=" * 70)
    print(f"SCENARIO: {name}")
    print("=" * 70)

    print("\n--- Applicant ---")
    print(f"Monthly Income: ₹{profile.monthly_income:,.2f}")
    print(
        f"Existing Obligations: "
        f"₹{profile.existing_obligations:,.2f}"
    )
    print(f"Loan Amount: ₹{profile.loan_amount:,.2f}")
    print(f"Credit Score: {profile.credit_score}")
    print(f"Previous Defaults: {profile.previous_defaults}")

    print("\n--- Financial Analyst ---")
    print(f"FOIR: {financial.foir:.2f}%")
    print(f"EMI: ₹{financial.emi:,.2f}")
    print(
        f"Remaining Income: "
        f"₹{financial.remaining_income:,.2f}"
    )
    print(f"Rule Risk: {financial.risk_level}")

    print("\n--- Risk Analyst ---")
    print(
        f"Default Probability: "
        f"{risk.default_probability:.4f}"
    )

    print("\n--- Lending Decision ---")
    print(f"Decision: {decision.decision}")
    print(f"Reason: {decision.reason}")

    print("\n--- Policy Retrieval ---")
    print(
        result.policy_analysis.policy_context
    )

    print("\n--- FINAL CREDIT ANALYST / GEMINI ---")
    print(result.analyst_explanation)


def main():
    for name, profile in SCENARIOS.items():
        evaluate_scenario(name, profile)


if __name__ == "__main__":
    main()