import logging

import litellm

from app.config import get_settings
from app.exceptions import WorkflowError
from app.providers.base import BaseLLMProvider
from app.providers.schema import LLMRequest, LLMResponse

logger = logging.getLogger(__name__)

# We use LiteLLM which natively wraps the standard OpenAI structure for multiple models
# Settings injection will be required to handle API keys globally or contextually.

from typing import AsyncGenerator


class OpenAIProvider(BaseLLMProvider):
    """
    Provider implementation that uses standard OpenAI SDK (via LiteLLM proxy)
    to connect to cloud LLMs (GPT-4o, Claude 3, etc.).
    """

    def __init__(self):
        settings = get_settings()
        self.api_key = settings.openai_api_key

    async def generate(self, request: LLMRequest) -> LLMResponse:
        if not self.api_key:
            raise WorkflowError("OpenAI API Key is not configured on the server.")

        logger.info(f"OpenAIProvider: Generating payload with model {request.model}")

        # Prepare LiteLLM messages
        api_messages = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]

        try:
            # We use litellm.acompletion for async network calls
            response = await litellm.acompletion(
                model=request.model,
                messages=api_messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                api_key=self.api_key.get_secret_value(),
            )

            content = response.choices[0].message.content
            usage = dict(response.usage) if response.usage else {}

            return LLMResponse(content=content or "", model=request.model, usage=usage)

        except Exception as e:
            logger.error(f"OpenAIProvider Generation Failed: {e}")
            raise WorkflowError(f"Cloud provider request failed: {str(e)}")

    async def generate_stream(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        if not self.api_key:
            raise WorkflowError("OpenAI API Key is not configured on the server.")

        logger.info(f"OpenAIProvider: Streaming payload with model {request.model}")

        api_messages = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]

        try:
            response_stream = await litellm.acompletion(
                model=request.model,
                messages=api_messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                api_key=self.api_key.get_secret_value(),
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
            logger.error(f"OpenAIProvider Streaming Failed: {e}")
            raise WorkflowError(f"Cloud provider stream failed: {str(e)}")

    async def health_check(self) -> bool:
        return bool(self.api_key)
