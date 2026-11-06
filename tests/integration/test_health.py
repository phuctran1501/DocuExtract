"""Integration tests for health endpoint and correlation ID middleware."""

from fastapi.testclient import TestClient

from app.core.correlation import CORRELATION_ID_HEADER


def test_health_endpoint_returns_ok(client: TestClient) -> None:
    """GET /health must return status 200 with the expected payload."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "ok", "service": "docuextract"}


def test_health_returns_correlation_id_header(client: TestClient) -> None:
    """Responses must include an X-Correlation-ID header."""
    response = client.get("/health")

    assert response.status_code == 200
    assert CORRELATION_ID_HEADER in response.headers
    correlation_id = response.headers[CORRELATION_ID_HEADER]
    assert len(correlation_id) > 0


def test_health_preserves_client_correlation_id(client: TestClient) -> None:
    """If client sends X-Correlation-ID, server must preserve and echo it."""
    client_id = "test-client-correlation-id-999"
    response = client.get(
        "/health",
        headers={CORRELATION_ID_HEADER: client_id},
    )

    assert response.status_code == 200
    assert response.headers.get(CORRELATION_ID_HEADER) == client_id


def test_not_found_returns_standard_error_envelope(client: TestClient) -> None:
    """Non-existent routes must return 404 with the standard error envelope."""
    client_id = "req-404-check"
    response = client.get(
        "/non-existent-path",
        headers={CORRELATION_ID_HEADER: client_id},
    )

    assert response.status_code == 404
    body = response.json()
    assert "error" in body
    error = body["error"]
    assert error["code"] == "NOT_FOUND"
    assert "Not Found" in error["message"]
    assert error["correlation_id"] == client_id

