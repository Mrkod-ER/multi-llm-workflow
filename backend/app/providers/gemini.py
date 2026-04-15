import logging
from typing import AsyncGenerator

import litellm

from app.config import get_settings
from app.exceptions import WorkflowError
from app.providers.base import BaseLLMProvider
from app.providers.schema import LLMRequest, LLMResponse

logger = logging.getLogger(__name__)


class GeminiProvider(BaseLLMProvider):
    """
    Provider implementation for Google Gemini models via LiteLLM.
    Supports Gemini 1.5 Pro, Gemini 1.5 Flash, and other Gemini variants.
    Requires GOOGLE_API_KEY in environment.
    """

    def __init__(self) -> None:
        settings = get_settings()
        self.api_key = settings.google_api_key

    def _prefixed_model(self, model: str) -> str:
        """Ensure model name has the gemini/ prefix LiteLLM expects."""
        if model.startswith("gemini/"):
            return model
        return f"gemini/{model}"

    async def generate(self, request: LLMRequest) -> LLMResponse:
        if not self.api_key:
            raise WorkflowError(
                "Google API Key is not configured. Set GOOGLE_API_KEY in your .env file."
            )

        model = self._prefixed_model(request.model)
        logger.info(f"GeminiProvider: Generating with model {model}")

        api_messages = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]

        try:
            response = await litellm.acompletion(
                model=model,
                messages=api_messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                api_key=self.api_key,
            )

            content = response.choices[0].message.content or ""
            usage = dict(response.usage) if response.usage else {}

            return LLMResponse(content=content, model=model, usage=usage)

        except Exception as e:
            logger.error(f"GeminiProvider generation failed: {e}")
            raise WorkflowError(f"Gemini request failed: {str(e)}")

    async def generate_stream(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        if not self.api_key:
            raise WorkflowError(
                "Google API Key is not configured. Set GOOGLE_API_KEY in your .env file."
            )

        model = self._prefixed_model(request.model)
        logger.info(f"GeminiProvider: Streaming with model {model}")

        api_messages = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]

        try:
            response_stream = await litellm.acompletion(
                model=model,
                messages=api_messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                api_key=self.api_key,
                stream=True,
            )

            async for chunk in response_stream:
                content = (
                    chunk.choices[0].delta.content
                    if chunk.choices and chunk.choices[0].delta
                    else None
                )
                if content:
                    yield content

        except Exception as e:
            logger.error(f"GeminiProvider streaming failed: {e}")
            raise WorkflowError(f"Gemini stream failed: {str(e)}")

    async def health_check(self) -> bool:
        return bool(self.api_key)
