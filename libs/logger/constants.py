"""Constants for the log package."""

# Log levels
LOG_LEVEL_DEBUG = "DEBUG"
LOG_LEVEL_INFO = "INFO"
LOG_LEVEL_WARNING = "WARNING"
LOG_LEVEL_ERROR = "ERROR"
LOG_LEVEL_CRITICAL = "CRITICAL"

# Environment variable names
ENV_LOG_LEVEL = "LOG_LEVEL"
ENV_LOG_PATH = "LOG_PATH"
ENV_LOG_ROTATION = "LOG_ROTATION"
ENV_LOG_RETENTION = "LOG_RETENTION"
ENV_LOG_COMPRESSION = "LOG_COMPRESSION"
ENV_LOG_CONSOLE_FORMAT = "LOG_CONSOLE_FORMAT"
ENV_LOG_FILE_FORMAT = "LOG_FILE_FORMAT"
ENV_LOG_APP_DIR = "LOG_APP_DIR"
ENV_LOG_ERROR_DIR = "LOG_ERROR_DIR"
ENV_LOG_DATE_FORMAT = "LOG_DATE_FORMAT"
ENV_APP_ENV = "APP_ENV"

# Default values
DEFAULT_LOG_LEVEL = LOG_LEVEL_INFO
DEFAULT_LOG_ROTATION = "10 MB"
DEFAULT_LOG_RETENTION = "1 week"
DEFAULT_LOG_COMPRESSION = "zip"
DEFAULT_LOG_DIR = "logs"
DEFAULT_APP_DIR = "application"
DEFAULT_ERROR_DIR = "error"
DEFAULT_DATE_FORMAT = "%Y-%m-%d"

# Default format strings
DEFAULT_CONSOLE_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

DEFAULT_FILE_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"

# Environment-specific log levels
ENV_LOG_LEVEL_LOCAL = LOG_LEVEL_DEBUG
ENV_LOG_LEVEL_DEV = LOG_LEVEL_INFO
ENV_LOG_LEVEL_PROD = LOG_LEVEL_WARNING

# Module-specific log levels
MODULE_LOG_LEVELS = {
    "app.api": LOG_LEVEL_DEBUG,
    "app.services": LOG_LEVEL_INFO,
    "app.repositories": LOG_LEVEL_WARNING,
    "main": LOG_LEVEL_DEBUG,
}
