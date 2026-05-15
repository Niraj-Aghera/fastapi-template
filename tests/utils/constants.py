"""Test constants for the application tests."""

__all__ = [
    "TEST_APPLICATION_NAME",
    "TEST_DB_HOST",
    "TEST_DB_NAME",
    "TEST_DB_USERNAME",
    "TEST_HOST",
    "TEST_PASSWORD",
    "TEST_PORT",
]

# Core test values - minimal set for essential functionality
TEST_DB_HOST = "localhost"
TEST_DB_USERNAME = "test_user"
TEST_DB_NAME = "test_db"
TEST_PASSWORD = "test_password"  # noqa: S105

# Application defaults
TEST_HOST = "0.0.0.0"  # noqa: S104
TEST_APPLICATION_NAME = "fastapi-template"
TEST_PORT = 5000
