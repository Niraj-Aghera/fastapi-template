"""Tests for LogConfig class and configuration methods."""

import os
from pathlib import Path
from unittest.mock import patch

from libs.logger.config import LogConfig
from libs.logger.constants import (
    DEFAULT_LOG_COMPRESSION,
    DEFAULT_LOG_LEVEL,
    DEFAULT_LOG_RETENTION,
    DEFAULT_LOG_ROTATION,
    ENV_APP_ENV,
    ENV_LOG_LEVEL,
    ENV_LOG_LEVEL_DEV,
    ENV_LOG_LEVEL_LOCAL,
    ENV_LOG_LEVEL_PROD,
    ENV_LOG_PATH,
)


# Mock AppEnv for testing
class MockAppEnv:
    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"


class TestLogConfig:
    """Test the LogConfig class methods."""

    def test_get_base_config(self):
        """Test that get_base_config returns expected default values."""
        config = LogConfig.get_base_config()

        assert config["default_level"] == DEFAULT_LOG_LEVEL
        assert config["rotation"] == DEFAULT_LOG_ROTATION
        assert config["retention"] == DEFAULT_LOG_RETENTION
        assert config["compression"] == DEFAULT_LOG_COMPRESSION
        assert "console_format" in config
        assert "file_format" in config
        assert "modules" in config
        assert isinstance(config["modules"], dict)

    def test_get_config_for_env_local(self):
        """Test environment-specific config for local environment."""
        config = LogConfig.get_config_for_env(MockAppEnv.LOCAL, "test_logs")

        assert config["log_path"] == "test_logs"
        assert config["default_level"] == ENV_LOG_LEVEL_LOCAL
        assert config["rotation"] == DEFAULT_LOG_ROTATION

    def test_get_config_for_env_dev(self):
        """Test environment-specific config for dev environment."""
        config = LogConfig.get_config_for_env(MockAppEnv.DEV, "dev_logs")

        assert config["log_path"] == "dev_logs"
        assert config["default_level"] == ENV_LOG_LEVEL_DEV

    def test_get_config_for_env_prod(self):
        """Test environment-specific config for prod environment."""
        config = LogConfig.get_config_for_env(MockAppEnv.PROD, "prod_logs")

        assert config["log_path"] == "prod_logs"
        assert config["default_level"] == ENV_LOG_LEVEL_PROD

    def test_get_config_for_env_string_values(self):
        """Test environment config with string values instead of enum."""
        config = LogConfig.get_config_for_env("local", "string_logs")
        assert config["default_level"] == ENV_LOG_LEVEL_LOCAL

        config = LogConfig.get_config_for_env("dev", "string_logs")
        assert config["default_level"] == ENV_LOG_LEVEL_DEV

        config = LogConfig.get_config_for_env("prod", "string_logs")
        assert config["default_level"] == ENV_LOG_LEVEL_PROD

    def test_get_fallback_config(self):
        """Test fallback configuration."""
        config = LogConfig.get_fallback_config()

        assert config["default_level"] == DEFAULT_LOG_LEVEL
        assert config["log_path"] == "logs"  # DEFAULT_LOG_DIR
        assert "rotation" in config
        assert "retention" in config
        assert "compression" in config


class TestLogConfigEnvironment:
    """Test LogConfig environment variable handling."""

    @patch.dict(os.environ, {}, clear=True)
    def test_from_env_defaults(self):
        """Test from_env with no environment variables set."""
        config = LogConfig.from_env()

        # When no env vars are set, it defaults to "local" environment
        # which sets log level to DEBUG, not INFO
        assert config["default_level"] == ENV_LOG_LEVEL_LOCAL
        assert isinstance(config["log_path"], Path)
        assert config["rotation"] == DEFAULT_LOG_ROTATION
        assert config["retention"] == DEFAULT_LOG_RETENTION
        assert config["compression"] == DEFAULT_LOG_COMPRESSION

    @patch.dict(
        os.environ,
        {
            ENV_LOG_LEVEL: "ERROR",
            ENV_LOG_PATH: "/custom/logs",
            "LOG_ROTATION": "50 MB",
            "LOG_RETENTION": "2 weeks",
        },
    )
    def test_from_env_custom_values(self):
        """Test from_env with custom environment variables."""
        config = LogConfig.from_env()

        assert config["default_level"] == "ERROR"
        assert str(config["log_path"]) == "/custom/logs"
        assert config["rotation"] == "50 MB"
        assert config["retention"] == "2 weeks"

    @patch.dict(os.environ, {ENV_APP_ENV: "local"}, clear=True)
    def test_from_env_app_env_local(self):
        """Test from_env with APP_ENV=local (no explicit LOG_LEVEL)."""
        config = LogConfig.from_env()
        assert config["default_level"] == ENV_LOG_LEVEL_LOCAL

    @patch.dict(os.environ, {ENV_APP_ENV: "dev"}, clear=True)
    def test_from_env_app_env_dev(self):
        """Test from_env with APP_ENV=dev (no explicit LOG_LEVEL)."""
        config = LogConfig.from_env()
        assert config["default_level"] == ENV_LOG_LEVEL_DEV

    @patch.dict(os.environ, {ENV_APP_ENV: "prod"}, clear=True)
    def test_from_env_app_env_prod(self):
        """Test from_env with APP_ENV=prod (no explicit LOG_LEVEL)."""
        config = LogConfig.from_env()
        assert config["default_level"] == ENV_LOG_LEVEL_PROD

    @patch.dict(
        os.environ,
        {
            ENV_LOG_LEVEL: "WARNING",  # Explicit LOG_LEVEL should override APP_ENV
            ENV_APP_ENV: "local",
        },
    )
    def test_from_env_explicit_log_level_overrides_app_env(self):
        """Test that explicit LOG_LEVEL overrides APP_ENV-based level."""
        config = LogConfig.from_env()
        assert config["default_level"] == "WARNING"  # Not ENV_LOG_LEVEL_LOCAL

    @patch.dict(
        os.environ,
        {"LOG_LEVEL": "DEBUG", "LOG_PATH": "/tmp/test_logs", "APP_ENV": "local"},
    )
    def test_environment_integration(self):
        """Test that environment variables are properly integrated."""
        # Re-import to get fresh config with new env vars
        import importlib

        import libs.logger.config

        importlib.reload(libs.logger.config)

        from libs.logger.config import default_config

        assert default_config["default_level"] == "DEBUG"
        assert str(default_config["log_path"]) == "/tmp/test_logs"
