"""Base exception classes for the application."""

from typing import Any


class BaseAppError(Exception):
    """Base exception class for all application exceptions."""

    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = 500,
        details: dict[str, Any] | None = None,
    ) -> None:
        """
        Initialize the base exception.

        Args:
            message: Human-readable error message
            error_code: Machine-readable error code
            status_code: HTTP status code
            details: Additional error details
        """
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details
        super().__init__(message)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the exception to a dictionary for API responses.

        Returns:
            Dictionary representation of the exception
        """
        error_dict: dict[str, Any] = {"code": self.error_code, "message": self.message}

        if self.details:
            error_dict["details"] = self.details

        return error_dict
