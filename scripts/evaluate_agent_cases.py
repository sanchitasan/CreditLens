from app.agents.credit_analyst_agent import (
    CreditAnalystAgent,
    CreditAnalystAgentInput,
)
from app.finance.profile import FinancialProfile
from app.llm.credit_analyst import CreditAnalyst
from app.llm.gemini_client import GeminiClient


def strong_profile() -> FinancialProfile:
    return FinancialProfile(
        monthly_income=80000,
        existing_obligations=20000,
        loan_amount=500000,
        annual_interest_rate=12,
        tenure_years=5,
        credit_score=780,
        employment_years=5,
        previous_defaults=0,
    )


def weak_profile() -> FinancialProfile:
    return FinancialProfile(
        monthly_income=50000,
        existing_obligations=29000,
        loan_amount=500000,
        annual_interest_rate=15,
        tenure_years=5,
        credit_score=680,
        employment_years=2,
        previous_defaults=2,
    )


def evaluate_case(agent, name, profile, expected_decision):

    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    result = agent.analyze(
        CreditAnalystAgentInput(profile=profile)
    )

    actual_decision = result.lending_decision.decision

    print(f"FOIR: {result.assessment.foir:.2f}%")
    print(
        f"Default probability: "
        f"{result.default_probability:.4f}"
    )
    print(f"Risk level: {result.assessment.risk_level}")
    print(f"Decision: {actual_decision}")
    print(f"Expected: {expected_decision}")

    print("\nPolicy sections retrieved:")
    print(result.policy_context.count("[Policy Context"))

    print("\nAnalyst explanation:")
    print(result.analyst_explanation)

    assert actual_decision == expected_decision

    return result


def main():

    analyst = CreditAnalyst(
        llm_client=GeminiClient()
    )

    agent = CreditAnalystAgent(
        analyst=analyst
    )

    evaluate_case(
        agent=agent,
        name="STRONG APPLICANT",
        profile=strong_profile(),
        expected_decision="APPROVE",
    )

    evaluate_case(
        agent=agent,
        name="WEAK APPLICANT",
        profile=weak_profile(),
        expected_decision="REJECT",
    )

    print("\n" + "=" * 70)
    print("ALL AGENT EVALUATIONS PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()