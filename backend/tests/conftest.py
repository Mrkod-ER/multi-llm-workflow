import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Synchronous test client for simple endpoint tests."""
    return TestClient(app)


from typing import AsyncGenerator
from httpx import ASGITransport

@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Asynchronous test client for async endpoint tests."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
