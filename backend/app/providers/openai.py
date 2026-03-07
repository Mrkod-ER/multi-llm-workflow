import litellm
import logging
from app.providers.base import BaseLLMProvider
from app.providers.schema import LLMRequest, LLMResponse
from app.config import get_settings
from app.exceptions import WorkflowError

logger = logging.getLogger(__name__)

# We use LiteLLM which natively wraps the standard OpenAI structure for multiple models
# Settings injection will be required to handle API keys globally or contextually.

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
        api_messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        try:
            # We use litellm.acompletion for async network calls
            response = await litellm.acompletion(
                model=request.model,
                messages=api_messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                api_key=self.api_key.get_secret_value()
            )
            
            content = response.choices[0].message.content
            usage = dict(response.usage) if response.usage else {}
            
            return LLMResponse(
                content=content or "",
                model=request.model,
                usage=usage
            )
            
        except Exception as e:
            logger.error(f"OpenAIProvider Generation Failed: {e}")
            raise WorkflowError(f"Cloud provider request failed: {str(e)}")

    async def health_check(self) -> bool:
        return bool(self.api_key)
