"""Integration tests for the text analysis API endpoint."""

from fastapi.testclient import TestClient

from app.core.correlation import CORRELATION_ID_HEADER


def test_analyze_text_success(client: TestClient) -> None:
    """POST /api/v1/text/analyze with valid input returns HTTP 200 and stats."""
    payload = {"text": "Text to analyze"}
    response = client.post("/api/v1/text/analyze", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data == {
        "character_count": 15,
        "word_count": 3,
        "line_count": 1,
    }
    assert CORRELATION_ID_HEADER in response.headers


def test_analyze_text_empty_string(client: TestClient) -> None:
    """POST /api/v1/text/analyze with empty text returns zeroes."""
    payload = {"text": ""}
    response = client.post("/api/v1/text/analyze", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data == {
        "character_count": 0,
        "word_count": 0,
        "line_count": 0,
    }


def test_analyze_text_multiline_vietnamese(client: TestClient) -> None:
    """POST /api/v1/text/analyze handles multiline Vietnamese text properly."""
    payload = {"text": "Họ và tên: Nguyễn Văn A\r\nVị trí: Kỹ sư Phần mềm"}
    response = client.post("/api/v1/text/analyze", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["word_count"] == 12
    assert data["line_count"] == 2


def test_analyze_text_missing_field(client: TestClient) -> None:
    """POST /api/v1/text/analyze with missing 'text' field returns HTTP 400."""
    response = client.post("/api/v1/text/analyze", json={})

    assert response.status_code == 400
    body = response.json()
    assert "error" in body
    assert body["error"]["code"] == "INVALID_REQUEST"


def test_analyze_text_preserves_correlation_id(client: TestClient) -> None:
    """POST /api/v1/text/analyze preserves the incoming X-Correlation-ID header."""
    client_id = "test-corr-text-123"
    response = client.post(
        "/api/v1/text/analyze",
        json={"text": "Hello world"},
        headers={CORRELATION_ID_HEADER: client_id},
    )

    assert response.status_code == 200
    assert response.headers.get(CORRELATION_ID_HEADER) == client_id
