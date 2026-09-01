from app.llm.credit_analyst import (
    CreditAnalystInput,
    build_credit_analyst_prompt,
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
    )

    prompt = build_credit_analyst_prompt(
        application
    )

    assert "Do not invent applicant information" in prompt
    assert "Do not recalculate EMI" in prompt
    assert "Do not override the lending decision" in prompt