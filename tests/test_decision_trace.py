from app.audit.decision_trace import DecisionTrace


def test_decision_trace_contract():

    financial = {
        "foir": 25.0,
        "emi": 11122.22,
        "remaining_income": 48877.78,
    }

    risk = {
        "default_probability": 0.03,
        "ml_explanation": [
            {
                "feature": "credit_score",
                "contribution": -3.9,
                "direction": "reduces default risk",
            }
        ],
    }

    decision = {
        "decision": "APPROVE",
        "reason": "Applicant has low credit risk.",
    }

    trace = DecisionTrace(
        applicant_data={
            "monthly_income": 80000,
            "existing_obligations": 20000,
            "loan_amount": 500000,
            "credit_score": 780,
            "previous_defaults": 0,
        },
        financial_analysis=financial,
        risk_analysis=risk,
        policy_context="FOIR policy guidance.",
        rule_risk_level="LOW",
        final_risk_level="LOW",
        lending_decision=decision,
        analyst_explanation="Final analyst explanation.",
    )

    assert trace.applicant_data["monthly_income"] == 80000

    assert trace.financial_analysis == financial

    assert trace.risk_analysis == risk

    assert trace.policy_context == "FOIR policy guidance."

    assert trace.rule_risk_level == "LOW"

    assert trace.final_risk_level == "LOW"

    assert trace.lending_decision == decision

    assert trace.analyst_explanation == (
        "Final analyst explanation."
    )