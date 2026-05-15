"""Unit tests for app.config.settings module."""

import os
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from app.config.settings import Settings
from tests.utils.constants import *

class TestSettings:
    """Test suite for application settings."""

    def test_defaults(self) -> None:
        """Test default values."""
        with patch.dict(
            os.environ,
            {
                "POSTGRES_DATABASE_HOST": TEST_DB_HOST,
                "POSTGRES_DATABASE_USERNAME": TEST_DB_USERNAME,
                "POSTGRES_DATABASE_PASSWORD": TEST_PASSWORD,
                "POSTGRES_DATABASE_NAME": TEST_DB_NAME,
            },
            clear=True,
        ):
            settings = Settings(_env_file=None)

            # Test app defaults
            assert settings.application_name == TEST_APPLICATION_NAME
            assert settings.host == TEST_HOST
            assert settings.port == TEST_PORT

            # Test database settings
            assert settings.postgres_database_host == TEST_DB_HOST
            assert settings.postgres_database_port == 5432
            assert settings.postgres_database_username == TEST_DB_USERNAME
            assert settings.postgres_database_password == TEST_PASSWORD
            assert settings.postgres_database_name == TEST_DB_NAME
            assert settings.postgres_database_echo is False

    def test_database_url(self) -> None:
        """Test database URL generation."""
        with patch.dict(
            os.environ,
            {
                "POSTGRES_DATABASE_HOST": TEST_DB_HOST,
                "POSTGRES_DATABASE_USERNAME": TEST_DB_USERNAME,
                "POSTGRES_DATABASE_PASSWORD": TEST_PASSWORD,
                "POSTGRES_DATABASE_NAME": TEST_DB_NAME,
            },
            clear=True,
        ):
            settings = Settings(_env_file=None)
            url = settings.postgres_database_url

            # Test URL format
            assert "postgresql+asyncpg://" in url
            assert TEST_DB_USERNAME in url
            assert TEST_PASSWORD in url
            assert TEST_DB_HOST in url
            assert TEST_DB_NAME in url

    def test_required_fields(self) -> None:
        """Test required database fields validation."""
        # Test missing host
        with (
            patch.dict(
                os.environ,
                {
                    "POSTGRES_DATABASE_USERNAME": TEST_DB_USERNAME,
                    "POSTGRES_DATABASE_PASSWORD": TEST_PASSWORD,
                    "POSTGRES_DATABASE_NAME": TEST_DB_NAME,
                },
                clear=True,
            ),
            pytest.raises(ValidationError),
        ):
            Settings(_env_file=None)

        # Test missing username
        with (
            patch.dict(
                os.environ,
                {
                    "POSTGRES_DATABASE_HOST": TEST_DB_HOST,
                    "POSTGRES_DATABASE_PASSWORD": TEST_PASSWORD,
                    "POSTGRES_DATABASE_NAME": TEST_DB_NAME,
                },
                clear=True,
            ),
            pytest.raises(ValidationError),
        ):
            Settings(_env_file=None)