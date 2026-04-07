import logging
from typing import AsyncGenerator

import httpx

from app.config import get_settings
from app.exceptions import WorkflowError
from app.providers.base import BaseLLMProvider
from app.providers.schema import LLMRequest, LLMResponse

logger = logging.getLogger(__name__)


class OllamaProvider(BaseLLMProvider):
    """
    Provider implementation that connects to a local Ollama instance
    via its native REST API using httpx.
    """

    def __init__(self):
        settings = get_settings()
        # Default Ollama port mapping from docker-compose is 11434
        self.base_url = settings.ollama_base_url.rstrip("/")

    async def generate(self, request: LLMRequest) -> LLMResponse:
        logger.info(
            f"OllamaProvider: Hitting {self.base_url} with model {request.model}"
        )

        url = f"{self.base_url}/api/chat"

        api_messages = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]

        payload = {
            "model": request.model,
            "messages": api_messages,
            "stream": False,
            "options": {"temperature": request.temperature},
        }

        # Simple retry with exponential backoff could be injected here
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                resp = await client.post(url, json=payload)
                resp.raise_for_status()
                data = resp.json()

                content = data.get("message", {}).get("content", "")

                # Ollama returns eval_count and prompt_eval_count
                usage = {
                    "prompt_tokens": data.get("prompt_eval_count", 0),
                    "completion_tokens": data.get("eval_count", 0),
                }

                return LLMResponse(content=content, model=request.model, usage=usage)
        except httpx.RequestError as e:
            logger.error(f"Ollama Network Error: {e}")
            raise WorkflowError(f"Ollama local provider request failed: {e}")

    async def generate_stream(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        import json

        logger.info(
            f"OllamaProvider: Streaming from {self.base_url} with model {request.model}"
        )

        url = f"{self.base_url}/api/chat"
        api_messages = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]

        payload = {
            "model": request.model,
            "messages": api_messages,
            "stream": True,
            "options": {"temperature": request.temperature},
        }

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                async with client.stream("POST", url, json=payload) as resp:
                    resp.raise_for_status()
                    async for line in resp.aiter_lines():
                        if line:
                            try:
                                data = json.loads(line)
                                content = data.get("message", {}).get("content")
                                if content:
                                    yield content
                            except json.JSONDecodeError:
                                pass
        except httpx.RequestError as e:
            logger.error(f"Ollama Streaming Network Error: {e}")
            raise WorkflowError(f"Ollama local provider stream failed: {e}")

    async def health_check(self) -> bool:
        url = f"{self.base_url}/api/tags"
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                res = await client.get(url)
                return res.status_code == 200
        except Exception:
            return False
