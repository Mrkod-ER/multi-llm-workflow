from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    """Test that the health check endpoint returns correctly."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_cors_headers(client: TestClient) -> None:
    """Test that CORS preflight requests are handled correctly."""
    headers = {
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type",
    }
    response = client.options("/health", headers=headers)
    assert response.status_code == 200
    assert (
        response.headers.get("access-control-allow-origin") == "http://localhost:3000"
    )
    assert "access-control-allow-methods" in response.headers
