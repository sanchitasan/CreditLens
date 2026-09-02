from types import SimpleNamespace

import app.agents.risk_analyst_agent as agent_module
from app.agents.risk_analyst_agent import (
    RiskAnalystAgent,
    RiskAnalystInput,
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


def test_risk_agent_calls_ml_prediction_and_explanation(
    monkeypatch,
):

    calls = []

    def fake_prediction(profile):
        calls.append("prediction")
        return 0.03

    def fake_explanation(profile):
        calls.append("explanation")
        return [
            {
                "feature": "credit_score",
                "contribution": -3.9,
                "direction": "reduces default risk",
            }
        ]

    monkeypatch.setattr(
        agent_module,
        "ml_prediction_tool",
        fake_prediction,
    )

    monkeypatch.setattr(
        agent_module,
        "ml_explanation_tool",
        fake_explanation,
    )

    profile = create_profile()

    agent = RiskAnalystAgent()

    result = agent.analyze(
        RiskAnalystInput(
            profile=profile
        )
    )

    assert calls == [
        "prediction",
        "explanation",
    ]

    assert result.default_probability == 0.03

    assert result.ml_explanation == [
        {
            "feature": "credit_score",
            "contribution": -3.9,
            "direction": "reduces default risk",
        }
    ]


def test_risk_agent_passes_profile_to_ml_tools(
    monkeypatch,
):

    received_prediction_profile = None
    received_explanation_profile = None

    def fake_prediction(profile):

        nonlocal received_prediction_profile

        received_prediction_profile = profile

        return 0.03

    def fake_explanation(profile):

        nonlocal received_explanation_profile

        received_explanation_profile = profile

        return []

    monkeypatch.setattr(
        agent_module,
        "ml_prediction_tool",
        fake_prediction,
    )

    monkeypatch.setattr(
        agent_module,
        "ml_explanation_tool",
        fake_explanation,
    )

    profile = create_profile()

    agent = RiskAnalystAgent()

    agent.analyze(
        RiskAnalystInput(
            profile=profile
        )
    )

    assert received_prediction_profile == profile
    assert received_explanation_profile == profile