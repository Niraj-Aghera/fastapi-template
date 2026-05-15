"""Authentication related exceptions."""

from typing import Any

from starlette.status import HTTP_403_FORBIDDEN

from app.exceptions.base_exceptions import BaseAppError

class ApiForbiddenError(BaseAppError):
    """Exception raised for API key authentication errors."""

    def __init__(self, error: str, message: str, details: dict[str, Any] | None = None) -> None:
        """
        Initialize the exception with an error code and message.

        Args:
            error: Error code for the exception
            message: Human-readable error message
            details: Additional error details
        """
        super().__init__(
            message=message,
            error_code=error,
            status_code=HTTP_403_FORBIDDEN,
            details=details,
        )