class CreditApplicationError(Exception):
    """
    Base exception for credit application failures.
    """

    def __init__(self, message: str):
        self.message = message

        super().__init__(message)

class CreditLensException(Exception):
    """Base exception for CreditLens."""


class ApplicationNotFoundError(CreditLensException):
    """Raised when a credit application does not exist."""

    def __init__(self, application_id: int):
        self.application_id = application_id

        super().__init__(
            f"Credit application {application_id} not found"
        )


class InvalidApplicationError(CreditLensException):
    """Raised when an application cannot be processed."""

    def __init__(self, message: str):
        super().__init__(message)