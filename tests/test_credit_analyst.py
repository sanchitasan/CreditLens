from app.llm.credit_analyst import (
    CreditAnalystInput,
    build_credit_analyst_prompt, CreditAnalyst,
)


def test_credit_analyst_prompt_contains_application_data():

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
        policy_context="FOIR above 50% is considered high risk."
    )

    prompt = build_credit_analyst_prompt(
        application
    )

    assert "80000" in prompt
    assert "500000" in prompt
    assert "750" in prompt
    assert "25.00%" in prompt
    assert "0.0268" in prompt
    assert "LOW" in prompt
    assert "APPROVE" in prompt
    assert "credit_score" in prompt


def test_credit_analyst_prompt_has_safety_rules():

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
        ml_explanation=[],
        lending_decision="APPROVE",
        decision_reason="Applicant has low credit risk.",
        policy_context="FOIR above 50% is considered high risk."
    )

    prompt = build_credit_analyst_prompt(
        application
    )

    assert "Do not invent applicant information" in prompt
    assert "Do not recalculate EMI" in prompt
    assert "Do not override the lending decision" in prompt
    assert "FOIR above 50% is considered high risk." in prompt

def test_credit_analyst_prompt_requires_policy_grounding():

    application = CreditAnalystInput(
        monthly_income=80000,
        existing_obligations=20000,
        loan_amount=500000,
        annual_interest_rate=12,
        tenure_years=5,
        credit_score=780,
        employment_years=5,
        previous_defaults=0,
        foir=25.0,
        emi=11122.22,
        total_obligations=31122.22,
        remaining_income=48877.78,
        risk_level="LOW",
        default_probability=0.0300,
        ml_explanation=[],
        lending_decision="APPROVE",
        decision_reason="Applicant has low credit risk.",
        policy_context=(
            "FOIR below 30%: Low financial obligation risk."
        ),
    )

    prompt = build_credit_analyst_prompt(application)

    assert (
        "Use the supplied POLICY CONTEXT as the policy reference"
        in prompt
    )

    assert (
        "Do not treat retrieved policy context as applicant data"
        in prompt
    )

    assert (
        "Do not infer policy thresholds or rules"
        in prompt
    )

    assert (
        "connect relevant applicant factors to the applicable policy context"
        in prompt
    )

    assert (
        "The lending decision and decision reason supplied by CreditLens remain authoritative"
        in prompt
    )

def test_credit_analyst_prompt_requires_policy_grounded_reasoning():

    application = CreditAnalystInput(
        monthly_income=50000,
        existing_obligations=29000,
        loan_amount=500000,
        annual_interest_rate=15,
        tenure_years=5,
        credit_score=680,
        employment_years=2,
        previous_defaults=2,
        foir=58.0,
        emi=11894.97,
        total_obligations=40894.97,
        remaining_income=9105.03,
        risk_level="HIGH",
        default_probability=0.2836,
        ml_explanation=[],
        lending_decision="REJECT",
        decision_reason="Applicant has high credit risk.",
        policy_context=(
            "FOIR above 50%: High financial obligation risk."
        ),
    )

    prompt = build_credit_analyst_prompt(application)

    assert "Policy-grounded reasoning" in prompt
    assert "Use only the supplied POLICY CONTEXT" in prompt
    assert "Do not invent missing policy thresholds or rules" in prompt
    assert "Do not change, reinterpret, or override" in prompt

def test_credit_analyst_sends_grounded_prompt_to_llm():

    class FakeLLMClient:

        def __init__(self):
            self.received_prompt = None

        def generate(self, prompt):
            self.received_prompt = prompt
            return "Grounded credit assessment."

    application = CreditAnalystInput(
        monthly_income=80000,
        existing_obligations=20000,
        loan_amount=500000,
        annual_interest_rate=12,
        tenure_years=5,
        credit_score=780,
        employment_years=5,
        previous_defaults=0,
        foir=25.0,
        emi=11122.22,
        total_obligations=31122.22,
        remaining_income=48877.78,
        risk_level="LOW",
        default_probability=0.0300,
        ml_explanation=[],
        lending_decision="APPROVE",
        decision_reason="Applicant has low credit risk.",
        policy_context=(
            "FOIR below 30%: Low financial obligation risk."
        ),
    )

    llm_client = FakeLLMClient()

    analyst = CreditAnalyst(
        llm_client=llm_client
    )

    result = analyst.analyze(application)

    assert result == "Grounded credit assessment."

    assert llm_client.received_prompt is not None

    assert (
        "FOIR below 30%: Low financial obligation risk."
        in llm_client.received_prompt
    )

    assert "APPROVE" in llm_client.received_prompt

    assert (
        "Do not override the lending decision"
        in llm_client.received_prompt
    )