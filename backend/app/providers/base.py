from abc import ABC, abstractmethod
from typing import AsyncGenerator

from app.providers.schema import LLMRequest, LLMResponse


class BaseLLMProvider(ABC):
    """Abstract base class dictating the interface for all LLM network providers."""

    @abstractmethod
    async def generate(self, request: LLMRequest) -> LLMResponse:
        """
        Sends the generation payload to the specific LLM API and formats the response.
        Raises specific ProviderError on network failures or invalid tokens.
        """
        pass

    @abstractmethod
    async def generate_stream(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        """
        Sends the generation payload and yields the response in incremental text chunks.
        """
        yield ""

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Pings the underlying network layer to make sure it's reachable.
        True if connected, Flase otherwise.
        """
        pass
