from app.finance import calculate_emi


def test_calculate_emi():
    result = calculate_emi(
        principal=500000,
        annual_interest_rate=12,
        tenure_years=5
    )

    assert round(result, 2) == 11122.22