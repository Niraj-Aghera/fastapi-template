"""Application environment enum."""

from app.utils.enums.base import BaseEnum


class AppEnv(BaseEnum):
    """Application environment enum.

    Using this enum instead of hardcoded strings helps avoid typos.
    """

    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"
