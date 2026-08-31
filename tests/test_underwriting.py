from app.services.underwriting import classify_risk


def test_low_risk():

    result = classify_risk(
        foir=25,
        remaining_income=50000,
        monthly_income=80000,
    )

    assert result["risk_level"] == "LOW"


def test_medium_risk():

    result = classify_risk(
        foir=45,
        remaining_income=22000,
        monthly_income=80000,
    )

    assert result["risk_level"] == "MEDIUM"


def test_high_risk():

    result = classify_risk(
        foir=60,
        remaining_income=10000,
        monthly_income=80000,
    )

    assert result["risk_level"] == "HIGH"