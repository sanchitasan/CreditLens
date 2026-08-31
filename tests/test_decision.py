import pytest

from app.services.decision import make_credit_decision


def test_low_risk_approve():

    result = make_credit_decision("LOW")

    assert result.decision == "APPROVE"
    assert result.reason == "Applicant has low credit risk."


def test_medium_risk_manual_review():

    result = make_credit_decision("MEDIUM")

    assert result.decision == "MANUAL_REVIEW"
    assert result.reason == "Applicant requires additional review."


def test_high_risk_reject():

    result = make_credit_decision("HIGH")

    assert result.decision == "REJECT"
    assert result.reason == "Applicant has high credit risk."


def test_invalid_risk_level():

    with pytest.raises(ValueError):

        make_credit_decision("UNKNOWN")