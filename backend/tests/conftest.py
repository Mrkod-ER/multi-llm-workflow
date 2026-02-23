import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient

from app.main import app

@pytest.fixture
def client() -> TestClient:
    """Synchronous test client for simple endpoint tests."""
    return TestClient(app)

@pytest.fixture
async def async_client() -> AsyncClient:
    """Asynchronous test client for async endpoint tests."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
