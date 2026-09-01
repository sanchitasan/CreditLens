from app.services.underwriting import combine_risk_assessment


def test_low_ml_probability_keeps_low_risk():

    result = combine_risk_assessment(
        rule_risk_level="LOW",
        default_probability=0.20,
    )

    assert result == "LOW"


def test_medium_ml_probability_increases_low_risk():

    result = combine_risk_assessment(
        rule_risk_level="LOW",
        default_probability=0.50,
    )

    assert result == "MEDIUM"


def test_high_ml_probability_creates_high_risk():

    result = combine_risk_assessment(
        rule_risk_level="LOW",
        default_probability=0.75,
    )

    assert result == "HIGH"


def test_high_rule_risk_is_not_reduced():

    result = combine_risk_assessment(
        rule_risk_level="HIGH",
        default_probability=0.20,
    )

    assert result == "HIGH"