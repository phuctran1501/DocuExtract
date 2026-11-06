"""Pytest fixtures for DocuExtract testing."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Test client fixture for making HTTP requests to the FastAPI application."""
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client

