import pytest

from app.providers.factory import ProviderFactory
from app.providers.mock import MockProvider
from app.providers.ollama import OllamaProvider
from app.providers.openai import OpenAIProvider
from app.providers.schema import ChatMessage, LLMProviderType, LLMRequest


def test_provider_factory_routing():
    assert isinstance(ProviderFactory.get_provider(LLMProviderType.MOCK), MockProvider)
    assert isinstance(ProviderFactory.get_provider("openai"), OpenAIProvider)
    assert isinstance(ProviderFactory.get_provider("ollama"), OllamaProvider)


def test_provider_factory_invalid():
    with pytest.raises(ValueError):
        ProviderFactory.get_provider("anthropic_direct")


@pytest.mark.asyncio
async def test_mock_provider():
    provider = ProviderFactory.get_provider(LLMProviderType.MOCK)
    req = LLMRequest(
        provider=LLMProviderType.MOCK,
        model="mock-model",
        messages=[ChatMessage(role="user", content="ping")],
    )

    resp = await provider.generate(req)
    assert "Mocked response" in resp.content
    assert "ping" in resp.content
    assert resp.model == "mock-model"
    assert resp.usage["total_tokens"] == 30
