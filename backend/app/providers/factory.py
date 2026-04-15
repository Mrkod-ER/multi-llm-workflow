from app.providers.base import BaseLLMProvider
from app.providers.gemini import GeminiProvider
from app.providers.mock import MockProvider
from app.providers.ollama import OllamaProvider
from app.providers.openai import OpenAIProvider
from app.providers.schema import LLMProviderType


class ProviderFactory:
    """Registry that instantiates and maps the correct LLM class."""

    _registry = {
        LLMProviderType.MOCK: MockProvider,
        LLMProviderType.OPENAI: OpenAIProvider,
        LLMProviderType.GEMINI: GeminiProvider,
        LLMProviderType.OLLAMA: OllamaProvider,
    }

    @classmethod
    def get_provider(cls, provider_type: LLMProviderType | str) -> BaseLLMProvider:
        """Returns instantiated provider logic based on requested enum type."""

        if isinstance(provider_type, str):
            provider_type = LLMProviderType(provider_type.lower())

        provider_class = cls._registry.get(provider_type)

        if not provider_class:
            raise ValueError(f"Unknown provider type: {provider_type}")

        return provider_class()  # type: ignore
