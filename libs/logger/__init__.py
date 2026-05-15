"""Log package for the application."""

from .config import LogConfig, default_config
from .constants import DEFAULT_LOG_LEVEL, ENV_LOG_LEVEL, ENV_LOG_PATH, LOG_LEVEL_DEBUG, LOG_LEVEL_ERROR, LOG_LEVEL_INFO, LOG_LEVEL_WARNING
from .handler import LogHandler, get_logger


__all__ = [
    # Common constants
    "DEFAULT_LOG_LEVEL",
    "ENV_LOG_LEVEL",
    "ENV_LOG_PATH",
    "LOG_LEVEL_DEBUG",
    "LOG_LEVEL_ERROR",
    "LOG_LEVEL_INFO",
    "LOG_LEVEL_WARNING",
    # Classes and functions
    "LogConfig",
    "LogHandler",
    "default_config",
    "get_logger",
]
