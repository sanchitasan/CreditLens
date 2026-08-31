import pytest

from app.finance import calculate_foir


def test_calculate_foir():
    result = calculate_foir(
        monthly_income=80000,
        monthly_obligations=20000
    )

    assert result == 25.0


def test_zero_obligations():
    result = calculate_foir(
        monthly_income=80000,
        monthly_obligations=0
    )

    assert result == 0.0


def test_high_obligations():
    result = calculate_foir(
        monthly_income=80000,
        monthly_obligations=60000
    )

    assert result == 75.0


def test_invalid_income():
    with pytest.raises(ValueError):
        calculate_foir(
            monthly_income=0,
            monthly_obligations=20000
        )