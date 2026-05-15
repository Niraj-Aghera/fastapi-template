"""Simple pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def app():
    """Create FastAPI app for testing."""
    from app.application import get_app

    return get_app()

@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)