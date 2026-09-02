from app.services.underwriting import combine_risk_assessment


def test_high_ml_probability_overrides_low_rule_risk():
    result = combine_risk_assessment(
        rule_risk_level="LOW",
        default_probability=0.70,
    )

    assert result == "HIGH"


def test_medium_ml_probability_escalates_low_rule_risk():
    result = combine_risk_assessment(
        rule_risk_level="LOW",
        default_probability=0.40,
    )

    assert result == "MEDIUM"


def test_low_ml_probability_preserves_rule_risk():
    result = combine_risk_assessment(
        rule_risk_level="LOW",
        default_probability=0.10,
    )

    assert result == "LOW"


def test_high_rule_risk_remains_high():
    result = combine_risk_assessment(
        rule_risk_level="HIGH",
        default_probability=0.10,
    )

    assert result == "HIGH"