from app.llm.credit_analyst import (
    CreditAnalyst,
    CreditAnalystInput,
)


class FakeLLMClient:
    """
    Fake LLM client used for testing.

    No external API call is made.
    """

    def __init__(self):
        self.received_prompt = None

    def generate(self, prompt: str) -> str:
        self.received_prompt = prompt

        return "Applicant has low credit risk and can be considered for approval."


def test_credit_analyst_uses_llm_client():

    llm_client = FakeLLMClient()

    analyst = CreditAnalyst(
        llm_client=llm_client
    )

    application = CreditAnalystInput(
        monthly_income=80000,
        existing_obligations=20000,
        loan_amount=500000,
        annual_interest_rate=12,
        tenure_years=5,
        credit_score=750,
        employment_years=4,
        previous_defaults=0,
        foir=25.0,
        emi=11122.22,
        total_obligations=31122.22,
        remaining_income=48877.78,
        risk_level="LOW",
        default_probability=0.0268,
        ml_explanation=[
            {
                "feature": "credit_score",
                "contribution": -3.2807,
                "direction": "reduces default risk",
            }
        ],
        lending_decision="APPROVE",
        decision_reason="Applicant has low credit risk.",
    )

    result = analyst.analyze(application)

    assert result == (
        "Applicant has low credit risk and can be considered for approval."
    )

    assert llm_client.received_prompt is not None
    assert "80000" in llm_client.received_prompt
    assert "750" in llm_client.received_prompt
    assert "0.0268" in llm_client.received_prompt