from typing import List, Dict, Any, Optional
from openai import OpenAI
import openai
from app.core.config import settings
from app.core.logger import logger
from app.core.exceptions import AIRateLimitError, AIError
from app.brain.providers.base import BaseLLMProvider

class GroqProvider(BaseLLMProvider):
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY not set in configuration")
            
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )
        self.model = "openai/gpt-oss-20b"

    def generate_response(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None) -> Any:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools if tools else None,
                max_tokens=500,
                temperature=0.7
            )
            return response
        except openai.RateLimitError as e:
            logger.error(f"Rate limit exceeded (429): {e}")
            raise AIRateLimitError("Groq's daily API limit has been reached. I'll pause AI requests until the limit resets.")
        except Exception as e:
            if "429" in str(e) or "rate_limit_exceeded" in str(e).lower():
                logger.error(f"Rate limit exceeded (429 string match): {e}")
                raise AIRateLimitError("Groq's daily API limit has been reached. I'll pause AI requests until the limit resets.")
            logger.error(f"AI API failure: {e}")
            raise AIError(f"Failed to generate response: {e}")

    def test_connection(self) -> bool:
        if not settings.OPENAI_API_KEY:
            return False
        return True
