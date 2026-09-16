from app.brain.providers.base import BaseLLMProvider
from app.brain.providers.groq_provider import GroqProvider
from app.brain.providers.ollama_provider import OllamaProvider
from app.brain.providers.hybrid_provider import HybridProvider
from app.core.config import settings
from app.core.logger import logger

def get_provider() -> BaseLLMProvider:
    provider_name = getattr(settings, "LLM_PROVIDER", "hybrid").lower()
    
    if provider_name == "ollama":
        return OllamaProvider()
    elif provider_name == "groq":
        return GroqProvider()
    
    # Default to hybrid if specified or unknown
    return HybridProvider()
