"""Tests for logger constants and their values."""

class TestLoggerConstants:
    """Test logger constants and their values."""

    def test_log_level_constants(self):
        """Test that log level constants have expected values."""
        from libs.logger.constants import LOG_LEVEL_CRITICAL, LOG_LEVEL_DEBUG, LOG_LEVEL_ERROR, LOG_LEVEL_INFO, LOG_LEVEL_WARNING

        assert LOG_LEVEL_DEBUG == "DEBUG"
        assert LOG_LEVEL_INFO == "INFO"
        assert LOG_LEVEL_WARNING == "WARNING"
        assert LOG_LEVEL_ERROR == "ERROR"
        assert LOG_LEVEL_CRITICAL == "CRITICAL"

    def test_environment_variable_constants(self):
        """Test environment variable name constants."""
        from libs.logger.constants import ENV_LOG_COMPRESSION, ENV_LOG_LEVEL, ENV_LOG_PATH, ENV_LOG_RETENTION, ENV_LOG_ROTATION

        assert ENV_LOG_LEVEL == "LOG_LEVEL"
        assert ENV_LOG_PATH == "LOG_PATH"
        assert ENV_LOG_ROTATION == "LOG_ROTATION"
        assert ENV_LOG_RETENTION == "LOG_RETENTION"
        assert ENV_LOG_COMPRESSION == "LOG_COMPRESSION"

    def test_default_value_constants(self):
        """Test default value constants."""
        from libs.logger.constants import (
            DEFAULT_LOG_COMPRESSION,
            DEFAULT_LOG_DIR,
            DEFAULT_LOG_LEVEL,
            DEFAULT_LOG_RETENTION,
            DEFAULT_LOG_ROTATION,
        )

        assert DEFAULT_LOG_LEVEL == "INFO"
        assert DEFAULT_LOG_ROTATION == "10 MB"
        assert DEFAULT_LOG_RETENTION == "1 week"
        assert DEFAULT_LOG_COMPRESSION == "zip"
        assert DEFAULT_LOG_DIR == "logs"

    def test_environment_specific_log_levels(self):
        """Test environment-specific log level constants."""
        from libs.logger.constants import ENV_LOG_LEVEL_DEV, ENV_LOG_LEVEL_LOCAL, ENV_LOG_LEVEL_PROD

        assert ENV_LOG_LEVEL_LOCAL == "DEBUG"
        assert ENV_LOG_LEVEL_DEV == "INFO"
        assert ENV_LOG_LEVEL_PROD == "WARNING"

    def test_module_log_levels(self):
        """Test module-specific log level configuration."""
        from libs.logger.constants import MODULE_LOG_LEVELS

        assert isinstance(MODULE_LOG_LEVELS, dict)
        assert "app.api" in MODULE_LOG_LEVELS
        assert "app.services" in MODULE_LOG_LEVELS
        assert "app.repositories" in MODULE_LOG_LEVELS
        assert "main" in MODULE_LOG_LEVELS

        # Test that all values are valid log levels
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        for module, level in MODULE_LOG_LEVELS.items():
            assert level in valid_levels, f"Invalid log level '{level}' for module '{module}'"

    def test_format_constants(self):
        """Test log format string constants."""
        from libs.logger.constants import DEFAULT_CONSOLE_FORMAT, DEFAULT_FILE_FORMAT

        # Test that format strings contain expected placeholders
        assert "{time" in DEFAULT_CONSOLE_FORMAT
        assert "{level" in DEFAULT_CONSOLE_FORMAT
        assert "{message}" in DEFAULT_CONSOLE_FORMAT

        assert "{time" in DEFAULT_FILE_FORMAT
        assert "{level" in DEFAULT_FILE_FORMAT
        assert "{message}" in DEFAULT_FILE_FORMAT

        # Console format should have color tags, file format should not
        assert "<green>" in DEFAULT_CONSOLE_FORMAT or "<level>" in DEFAULT_CONSOLE_FORMAT
        assert "<green>" not in DEFAULT_FILE_FORMAT

    def test_directory_constants(self):
        """Test directory name constants."""
        from libs.logger.constants import DEFAULT_APP_DIR, DEFAULT_DATE_FORMAT, DEFAULT_ERROR_DIR

        assert DEFAULT_APP_DIR == "application"
        assert DEFAULT_ERROR_DIR == "error"
        assert DEFAULT_DATE_FORMAT == "%Y-%m-%d"