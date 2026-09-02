import pytest

from app.services.exceptions import (
    CreditLensException,
    CreditApplicationError,
    ApplicationNotFoundError,
    InvalidApplicationError,
)


def test_credit_application_error_is_creditlens_exception():
    error = CreditApplicationError(
        "Invalid credit application"
    )

    assert isinstance(
        error,
        CreditLensException,
    )


def test_application_not_found_error_is_creditlens_exception():
    error = ApplicationNotFoundError(123)

    assert isinstance(
        error,
        CreditLensException,
    )

    assert error.application_id == 123
    assert str(error) == (
        "Credit application 123 not found"
    )


def test_invalid_application_error_is_creditlens_exception():
    error = InvalidApplicationError(
        "Invalid application"
    )

    assert isinstance(
        error,
        CreditLensException,
    )

    assert str(error) == "Invalid application"


def test_creditlens_exception_can_be_caught_as_base_exception():
    with pytest.raises(CreditLensException):
        raise CreditApplicationError(
            "Application processing failed"
        )