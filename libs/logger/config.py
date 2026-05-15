"""Centralized log configuration with environment awareness."""

import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

from .constants import (
    DEFAULT_APP_DIR,
    DEFAULT_CONSOLE_FORMAT,
    DEFAULT_DATE_FORMAT,
    DEFAULT_ERROR_DIR,
    DEFAULT_FILE_FORMAT,
    DEFAULT_LOG_COMPRESSION,
    DEFAULT_LOG_DIR,
    DEFAULT_LOG_LEVEL,
    DEFAULT_LOG_RETENTION,
    DEFAULT_LOG_ROTATION,
    ENV_APP_ENV,
    ENV_LOG_APP_DIR,
    ENV_LOG_COMPRESSION,
    ENV_LOG_CONSOLE_FORMAT,
    ENV_LOG_DATE_FORMAT,
    ENV_LOG_ERROR_DIR,
    ENV_LOG_FILE_FORMAT,
    ENV_LOG_LEVEL,
    ENV_LOG_LEVEL_DEV,
    ENV_LOG_LEVEL_LOCAL,
    ENV_LOG_LEVEL_PROD,
    ENV_LOG_PATH,
    ENV_LOG_RETENTION,
    ENV_LOG_ROTATION,
    MODULE_LOG_LEVELS,
)


if TYPE_CHECKING:
    from app.appenv import AppEnv
else:
    # Runtime placeholder for vulture
    AppEnv = None


class LogConfig:
    """Single source of truth for log configuration (defaults + env-aware)."""

    # Base defaults from constants
    DEFAULT_LEVEL = DEFAULT_LOG_LEVEL
    ROTATION = DEFAULT_LOG_ROTATION
    RETENTION = DEFAULT_LOG_RETENTION
    COMPRESSION = DEFAULT_LOG_COMPRESSION

    # Format strings
    CONSOLE_FORMAT = DEFAULT_CONSOLE_FORMAT
    FILE_FORMAT = DEFAULT_FILE_FORMAT

    # Module configurations from constants
    MODULES: ClassVar[dict[str, dict[str, str]]] = {module: {"level": level} for module, level in MODULE_LOG_LEVELS.items()}

    @classmethod
    def get_base_config(cls) -> dict[str, Any]:
        """Return default (static) configuration."""
        return {
            "default_level": cls.DEFAULT_LEVEL,
            "rotation": cls.ROTATION,
            "retention": cls.RETENTION,
            "compression": cls.COMPRESSION,
            "console_format": cls.CONSOLE_FORMAT,
            "file_format": cls.FILE_FORMAT,
            "modules": cls.MODULES,
        }

    @classmethod
    def get_config_for_env(cls, env: "AppEnv", log_path: str = "logs") -> dict[str, Any]:
        """Return defaults adapted to a specific env enum/string."""
        config = cls.get_base_config()
        config["log_path"] = log_path

        env_value = env.value if hasattr(env, "value") else str(env)
        if env_value == "local":
            config["default_level"] = ENV_LOG_LEVEL_LOCAL
        elif env_value == "dev":
            config["default_level"] = ENV_LOG_LEVEL_DEV
        elif env_value == "prod":
            config["default_level"] = ENV_LOG_LEVEL_PROD

        return config

    @classmethod
    def get_fallback_config(cls) -> dict[str, Any]:
        """Return default configuration with a default log directory."""
        return {
            "default_level": cls.DEFAULT_LEVEL,
            "log_path": DEFAULT_LOG_DIR,
            "rotation": cls.ROTATION,
            "retention": cls.RETENTION,
            "compression": cls.COMPRESSION,
            "console_format": cls.CONSOLE_FORMAT,
            "file_format": cls.FILE_FORMAT,
            "modules": cls.MODULES,
        }

    @classmethod
    def from_env(cls) -> dict[str, Any]:
        """Return environment-aware configuration using env vars."""
        base_dir = Path(__file__).parent.parent.parent

        log_level = os.getenv(ENV_LOG_LEVEL, DEFAULT_LOG_LEVEL)
        log_path = Path(os.getenv(ENV_LOG_PATH, base_dir / DEFAULT_LOG_DIR))
        log_rotation = os.getenv(ENV_LOG_ROTATION, DEFAULT_LOG_ROTATION)
        log_retention = os.getenv(ENV_LOG_RETENTION, DEFAULT_LOG_RETENTION)
        log_compression = os.getenv(ENV_LOG_COMPRESSION, DEFAULT_LOG_COMPRESSION)

        console_format = os.getenv(ENV_LOG_CONSOLE_FORMAT, DEFAULT_CONSOLE_FORMAT)
        file_format = os.getenv(ENV_LOG_FILE_FORMAT, DEFAULT_FILE_FORMAT)
        app_dir = os.getenv(ENV_LOG_APP_DIR, DEFAULT_APP_DIR)
        error_dir = os.getenv(ENV_LOG_ERROR_DIR, DEFAULT_ERROR_DIR)
        date_format = os.getenv(ENV_LOG_DATE_FORMAT, DEFAULT_DATE_FORMAT)

        app_env = os.getenv(ENV_APP_ENV, "local").lower()
        if ENV_LOG_LEVEL not in os.environ:
            if app_env == "local":
                log_level = ENV_LOG_LEVEL_LOCAL
            elif app_env == "dev":
                log_level = ENV_LOG_LEVEL_DEV
            elif app_env == "prod":
                log_level = ENV_LOG_LEVEL_PROD

        return {
            "default_level": log_level,
            "log_path": log_path,
            "rotation": log_rotation,
            "retention": log_retention,
            "compression": log_compression,
            "console_format": console_format,
            "file_format": file_format,
            "app_dir": app_dir,
            "error_dir": error_dir,
            "date_format": date_format,
            "modules": MODULE_LOG_LEVELS,
        }


# Default env-aware configuration
default_config = LogConfig.from_env()
