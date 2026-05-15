"""Integration tests for the complete logger package."""

from unittest.mock import patch


class TestLoggerIntegration:
    """Test the complete logger integration."""

    def test_get_logger_function_import(self):
        """Test that get_logger function can be imported."""
        from libs.logger import get_logger

        assert callable(get_logger)

    def test_default_config_import(self):
        """Test that default_config can be imported."""
        from libs.logger import default_config

        assert isinstance(default_config, dict)
        assert "default_level" in default_config

    def test_log_config_import(self):
        """Test that LogConfig class can be imported."""
        from libs.logger import LogConfig

        assert LogConfig is not None

    @patch("libs.logger.handler.logger")
    def test_logger_package_exports(self, mock_logger):
        """Test that all expected exports are available."""
        from libs.logger import (
            DEFAULT_LOG_LEVEL,
            ENV_LOG_LEVEL,
            ENV_LOG_PATH,
            LOG_LEVEL_DEBUG,
            LOG_LEVEL_ERROR,
            LOG_LEVEL_INFO,
            LOG_LEVEL_WARNING,
            LogConfig,
            LogHandler,
            default_config,
            get_logger,
        )

        # Test that all imports work
        assert callable(get_logger)
        assert LogHandler is not None
        assert LogConfig is not None
        assert isinstance(default_config, dict)

        # Test constants
        assert LOG_LEVEL_DEBUG == "DEBUG"
        assert LOG_LEVEL_INFO == "INFO"
        assert LOG_LEVEL_WARNING == "WARNING"
        assert LOG_LEVEL_ERROR == "ERROR"
        assert ENV_LOG_LEVEL == "LOG_LEVEL"
        assert ENV_LOG_PATH == "LOG_PATH"
        assert DEFAULT_LOG_LEVEL == "INFO"

    def test_logger_package_all_exports(self):
        """Test that __all__ contains expected exports."""
        from libs.logger import __all__

        expected_exports = [
            "get_logger",
            "LogHandler",
            "LogConfig",
            "default_config",
            "LOG_LEVEL_DEBUG",
            "LOG_LEVEL_INFO",
            "LOG_LEVEL_WARNING",
            "LOG_LEVEL_ERROR",
            "ENV_LOG_LEVEL",
            "ENV_LOG_PATH",
            "DEFAULT_LOG_LEVEL",
        ]

        for export in expected_exports:
            assert export in __all__, f"Missing export: {export}"

    @patch("libs.logger.handler.logger")
    def test_get_logger_returns_bound_logger(self, mock_logger):
        """Test that get_logger returns a properly bound logger."""
        from libs.logger import get_logger

        # Mock the bound logger
        mock_bound_logger = mock_logger.bind.return_value

        logger = get_logger("test.module")

        # Verify logger.bind was called with correct name
        mock_logger.bind.assert_called_once_with(name="test.module")

        # Verify we get the bound logger back
        assert logger == mock_bound_logger

    def test_default_config_structure(self):
        """Test that default_config has expected structure."""
        from libs.logger import default_config

        required_keys = [
            "default_level",
            "log_path",
            "rotation",
            "retention",
            "compression",
            "console_format",
            "file_format",
            "app_dir",
            "error_dir",
            "date_format",
            "modules",
        ]

        for key in required_keys:
            assert key in default_config, f"Missing key in default_config: {key}"

        # Test specific value types
        assert isinstance(default_config["modules"], dict)
        assert isinstance(default_config["default_level"], str)
        assert isinstance(default_config["console_format"], str)
        assert isinstance(default_config["file_format"], str)


class TestLoggerBackwardCompatibility:
    """Test backward compatibility with previous logger versions."""

    def test_basic_usage_pattern(self):
        """Test that basic usage pattern still works."""
        from libs.logger import get_logger

        # This should work without errors
        logger = get_logger(__name__)
        assert logger is not None

    def test_config_access_pattern(self):
        """Test that config access patterns work."""
        from libs.logger import LogConfig, default_config

        # These should work without errors
        base_config = LogConfig.get_base_config()
        fallback_config = LogConfig.get_fallback_config()

        assert isinstance(base_config, dict)
        assert isinstance(fallback_config, dict)
        assert isinstance(default_config, dict)

    @patch("libs.logger.handler.logger")
    def test_handler_instantiation_patterns(self, mock_logger):
        """Test that handler instantiation patterns work."""
        from libs.logger import LogHandler, default_config

        with patch("os.makedirs"):
            # Default instantiation
            handler1 = LogHandler()
            assert handler1 is not None

            # Custom config instantiation
            handler2 = LogHandler(default_config)
            assert handler2 is not None

            # Custom config dict instantiation
            custom_config = {"default_level": "DEBUG", "log_path": "/tmp"}
            handler3 = LogHandler(custom_config)
            assert handler3 is not None
