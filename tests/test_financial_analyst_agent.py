from types import SimpleNamespace

import app.agents.financial_analyst_agent as agent_module
from app.agents.financial_analyst_agent import (
    FinancialAnalystAgent,
    FinancialAnalystInput,
)
from app.finance.profile import FinancialProfile


def create_profile():
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


def test_financial_agent_delegates_to_assessment_tool(
    monkeypatch,
):

    fake_assessment = SimpleNamespace(
        foir=25.0,
        emi=11122.22,
        total_obligations=31122.22,
        remaining_income=48877.78,
        risk_level="LOW",
        risk_reasons=[
            "Applicant passes basic financial rules"
        ],
    )

    received_profile = None

    def fake_credit_assessment_tool(profile):

        nonlocal received_profile

        received_profile = profile

        return fake_assessment

    monkeypatch.setattr(
        agent_module,
        "credit_assessment_tool",
        fake_credit_assessment_tool,
    )

    profile = create_profile()

    agent = FinancialAnalystAgent()

    result = agent.analyze(
        FinancialAnalystInput(
            profile=profile
        )
    )

    assert received_profile == profile

    assert result.foir == 25.0
    assert result.emi == 11122.22
    assert result.total_obligations == 31122.22
    assert result.remaining_income == 48877.78
    assert result.risk_level == "LOW"

    assert result.risk_reasons == [
        "Applicant passes basic financial rules"
    ]


def test_financial_agent_returns_financial_analysis():

    profile = create_profile()

    fake_assessment = SimpleNamespace(
        foir=25.0,
        emi=11122.22,
        total_obligations=31122.22,
        remaining_income=48877.78,
        risk_level="LOW",
        risk_reasons=[
            "Applicant passes basic financial rules"
        ],
    )

    original_tool = agent_module.credit_assessment_tool

    agent_module.credit_assessment_tool = (
        lambda profile: fake_assessment
    )

    try:
        agent = FinancialAnalystAgent()

        result = agent.analyze(
            FinancialAnalystInput(
                profile=profile
            )
        )

        assert result.foir == 25.0
        assert result.risk_level == "LOW"

    finally:
        agent_module.credit_assessment_tool = original_tool