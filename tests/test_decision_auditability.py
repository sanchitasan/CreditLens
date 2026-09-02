from app.services.underwriting import combine_risk_assessment
from app.services.decision import make_credit_decision


def test_low_risk_low_ml_probability_approves():
    final_risk = combine_risk_assessment(
        rule_risk_level="LOW",
        default_probability=0.03,
    )

    decision = make_credit_decision(
        risk_level=final_risk,
        default_probability=0.03,
    )

    assert final_risk == "LOW"
    assert decision.decision == "APPROVE"


def test_medium_rule_risk_requires_manual_review():
    final_risk = combine_risk_assessment(
        rule_risk_level="MEDIUM",
        default_probability=0.05,
    )

    decision = make_credit_decision(
        risk_level=final_risk,
        default_probability=0.05,
    )

    assert final_risk == "MEDIUM"
    assert decision.decision == "MANUAL_REVIEW"


def test_high_rule_risk_rejects():
    final_risk = combine_risk_assessment(
        rule_risk_level="HIGH",
        default_probability=0.28,
    )

    decision = make_credit_decision(
        risk_level=final_risk,
        default_probability=0.28,
    )

    assert final_risk == "HIGH"
    assert decision.decision == "REJECT"


def test_high_ml_probability_escalates_low_rule_risk():
    final_risk = combine_risk_assessment(
        rule_risk_level="LOW",
        default_probability=0.70,
    )

    decision = make_credit_decision(
        risk_level=final_risk,
        default_probability=0.70,
    )

    assert final_risk == "HIGH"
    assert decision.decision == "REJECT"