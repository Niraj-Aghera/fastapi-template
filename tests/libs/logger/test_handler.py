"""Tests for LogHandler class and logging functionality."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch


class TestLogHandler:
    """Test the LogHandler class functionality."""

    def test_log_handler_import(self):
        """Test that LogHandler can be imported without errors."""
        from libs.logger.handler import LogHandler

        assert LogHandler is not None

    @patch("libs.logger.handler.logger")
    def test_log_handler_initialization_with_config(self, mock_logger):
        """Test LogHandler initialization with custom config."""
        from libs.logger.handler import LogHandler

        custom_config = {
            "default_level": "DEBUG",
            "log_path": "/tmp/test_logs",
            "app_dir": "test_app",
            "error_dir": "test_error",
            "date_format": "%Y-%m-%d",
        }

        with patch("os.makedirs"):
            handler = LogHandler(custom_config)

        assert handler.config == custom_config
        assert str(handler.base_log_path) == "/tmp/test_logs"

    @patch("libs.logger.handler.logger")
    def test_log_handler_initialization_default_config(self, mock_logger):
        """Test LogHandler initialization with default config."""
        from libs.logger.handler import LogHandler

        with patch("os.makedirs"):
            handler = LogHandler()

        # Handler should have a valid config when no config is provided
        assert handler.config is not None
        assert "default_level" in handler.config
        assert "log_path" in handler.config
        assert "rotation" in handler.config

    @patch("libs.logger.handler.logger")
    def test_get_logger_static_method(self, mock_logger):
        """Test the static get_logger method."""
        from libs.logger.handler import LogHandler

        mock_logger.bind.return_value = MagicMock()

        logger_instance = LogHandler.get_logger("test_module")

        mock_logger.bind.assert_called_once_with(name="test_module")
        assert logger_instance is not None

    def test_log_handler_directory_creation(self):
        """Test that LogHandler creates necessary directories."""
        from libs.logger.handler import LogHandler

        with tempfile.TemporaryDirectory() as temp_dir:
            custom_config = {
                "log_path": temp_dir,
                "app_dir": "application",
                "error_dir": "error",
            }

            with patch("libs.logger.handler.logger"):
                handler = LogHandler(custom_config)

            app_logs_dir = Path(temp_dir) / "application"
            error_logs_dir = Path(temp_dir) / "error"

            assert app_logs_dir.exists()
            assert error_logs_dir.exists()
            assert handler.app_logs_dir == app_logs_dir
            assert handler.error_logs_dir == error_logs_dir


class TestLogHandlerFileOperations:
    """Test LogHandler file operations and setup."""

    def test_log_file_structure_creation(self):
        """Test that log files and directories are created correctly."""
        from libs.logger.handler import LogHandler

        with tempfile.TemporaryDirectory() as temp_dir:
            custom_config = {
                "log_path": temp_dir,
                "app_dir": "application",
                "error_dir": "error",
                "default_level": "INFO",
            }

        with patch("libs.logger.handler.logger") as mock_logger:
            _ = LogHandler(custom_config)

            # Verify directories were created
            app_dir = Path(temp_dir) / "application"
            error_dir = Path(temp_dir) / "error"

            assert app_dir.exists()
            assert error_dir.exists()

            # Verify logger.add was called for console, app, and error logs
            assert mock_logger.remove.called
            assert mock_logger.add.call_count >= 3  # console + app + error

    @patch("libs.logger.handler.logger")
    def test_logger_setup_calls(self, mock_logger):
        """Test that logger setup methods are called correctly."""
        from libs.logger.handler import LogHandler

        custom_config = {
            "default_level": "DEBUG",
            "console_format": "test console format",
            "file_format": "test file format",
        }

        with patch("os.makedirs"):
            LogHandler(custom_config)

        # Verify logger.remove was called to clear default handlers
        mock_logger.remove.assert_called_once()

        # Verify logger.add was called multiple times for different handlers
        assert mock_logger.add.call_count >= 3

        # Check that the calls include our custom formats
        add_calls = mock_logger.add.call_args_list
        format_args = [call[1].get("format") for call in add_calls if "format" in call[1]]

        assert any("test console format" in str(fmt) for fmt in format_args)
        assert any("test file format" in str(fmt) for fmt in format_args)
