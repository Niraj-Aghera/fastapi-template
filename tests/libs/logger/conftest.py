"""Logger-specific test configuration that doesn't depend on database settings."""

# This conftest.py overrides the parent conftest.py for logger tests
# to avoid database configuration issues that aren't relevant to logger testing

import pytest


# Disable the problematic test_settings fixture from parent conftest.py
@pytest.fixture(scope="session", autouse=True)
def test_settings():
    """Override parent test_settings fixture to avoid database config issues."""
    # Return None since logger tests don't need app settings
    return
