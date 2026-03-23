import asyncio
from typing import AsyncGenerator
from app.providers.base import BaseLLMProvider
from app.providers.schema import LLMRequest, LLMResponse

class MockProvider(BaseLLMProvider):
    """
    Simulates an LLM response without making network calls.
    Useful for testing workflow graph integrity and running fast unit tests.
    """
    async def generate(self, request: LLMRequest) -> LLMResponse:
        # Simulate network latency
        await asyncio.sleep(0.5)
        
        last_message = request.messages[-1].content if request.messages else ""
        mocked_text = f"Mocked response for '{last_message}' using {request.model}"
        
        return LLMResponse(
            content=mocked_text,
            model=request.model,
            usage={"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
        )
        
    async def generate_stream(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        # Simulate network latency
        await asyncio.sleep(0.2)
        
        last_message = request.messages[-1].content if request.messages else ""
        mocked_text = f"Mocked response for '{last_message}' using {request.model}"
        
        words = mocked_text.split(" ")
        for i, word in enumerate(words):
            await asyncio.sleep(0.1) # Simulate typing delay
            yield word + (" " if i < len(words) - 1 else "")
        
    async def health_check(self) -> bool:
        return True
