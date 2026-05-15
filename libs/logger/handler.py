"""Log handler for the application."""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from loguru import logger

# Import unified config
from .config import LogConfig, default_config


# Default log path
DEFAULT_LOG_PATH = Path("logs")


class LogHandler:
    """
    LogHandler class to manage loguru log configurations.
    Allows setting different log levels for different modules.
    """

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """
        Initialize the LogHandler with configuration.

        Args:
            config: Dictionary containing log configuration.
                   If None, default configuration will be used.
        """
        self.config = config or default_config
        self.base_log_path = Path(self.config.get("log_path", DEFAULT_LOG_PATH))

        # Create logs directory structure using configurable names
        app_dir = self.config.get("app_dir", "application")
        error_dir = self.config.get("error_dir", "error")
        self.app_logs_dir = self.base_log_path / app_dir
        self.error_logs_dir = self.base_log_path / error_dir

        self.app_logs_dir.mkdir(parents=True, exist_ok=True)
        self.error_logs_dir.mkdir(parents=True, exist_ok=True)

        # Get current date for day-wise log organization using configurable format
        date_format = self.config.get("date_format", "%Y-%m-%d")
        self.current_date = datetime.now().strftime(date_format)

        # Remove default logger
        logger.remove()

        # Set up default configurations
        self._setup_default_loggers()

    def _setup_default_loggers(self) -> None:
        """Set up default loggers for console and file output."""
        # Console logger
        log_level = self.config.get("default_level", LogConfig.DEFAULT_LEVEL)
        logger.add(
            sys.stderr,
            format=self.config.get("console_format", LogConfig.CONSOLE_FORMAT),
            level=log_level,
            colorize=True,
        )

        # File logger for all logs in application directory
        logger.add(
            self.app_logs_dir / f"{self.current_date}.log",
            format=self.config.get("file_format", LogConfig.FILE_FORMAT),
            level=log_level,
            rotation=self.config.get("rotation", LogConfig.ROTATION),
            retention=self.config.get("retention", LogConfig.RETENTION),
            compression=self.config.get("compression", LogConfig.COMPRESSION),
        )

        # File logger for errors only in error directory
        logger.add(
            self.error_logs_dir / f"{self.current_date}.log",
            format=self.config.get("file_format", LogConfig.FILE_FORMAT),
            level="ERROR",
            rotation=self.config.get("rotation", LogConfig.ROTATION),
            retention=self.config.get("retention", LogConfig.RETENTION),
            compression=self.config.get("compression", LogConfig.COMPRESSION),
        )

    @staticmethod
    def get_logger(name: str) -> Any:
        """
        Get a logger for a specific module.

        Args:
            name: The name of the module.

        Returns:
            A loguru logger instance.
        """
        return logger.bind(name=name)


# Initialize the log handler with default configuration
log_handler = LogHandler()

# Export the get_logger function for easy access
get_logger = log_handler.get_logger
