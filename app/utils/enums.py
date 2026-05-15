"""Enums for the application."""

from enum import Enum
from typing import Self, TypeVar


T = TypeVar("T", bound="BaseEnum")


class BaseEnum(str, Enum):
    """Base enum class with common functionality for all application enums.

    This class provides common methods that can be used by all enum types
    in the application, reducing code duplication and ensuring consistent
    behavior across different enum types.
    """

    @classmethod
    def list(cls) -> list[str]:
        """Return a list of all enum values."""
        return [item.value for item in cls]

    @classmethod
    def is_valid(cls, value: str) -> bool:
        """Check if the given value is valid for this enum."""
        return value in cls.list()

    @classmethod
    def from_value(cls, value: str) -> Self:
        """Get enum member from string value.

        Args:
            value: The string value to convert to enum

        Returns:
            The corresponding enum member

        Raises:
            ValueError: If the value is not valid for this enum
        """
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"'{value}' is not a valid {cls.__name__} value")

    def __str__(self) -> str:
        """String representation of the enum value."""
        return str(self.value)
