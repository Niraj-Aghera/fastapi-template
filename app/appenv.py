"""Application environment enum."""

from app.utils.enums import BaseEnum


class AppEnv(BaseEnum):
    """Application environment enum.

    This enum represents the different environments in which the application can run.
    Using this enum instead of hardcoded strings helps avoid typos.
    """

    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"
