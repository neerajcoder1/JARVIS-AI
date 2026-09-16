from typing import List, Dict, Any, Optional
from app.core.logger import logger
from app.core.exceptions import AIRateLimitError, AIError
from app.brain.providers.base import BaseLLMProvider
from app.brain.providers.groq_provider import GroqProvider
from app.brain.providers.ollama_provider import OllamaProvider

class ProviderMetrics:
    def __init__(self):
        self.ollama_requests = 0
        self.groq_requests = 0
        self.total_requests = 0
        # Optional: could track token approximations if needed
        self.ollama_successes = 0
        self.groq_successes = 0

metrics = ProviderMetrics()

class HybridProvider(BaseLLMProvider):
    def __init__(self):
        self.groq = GroqProvider()
        self.ollama = OllamaProvider()
        
    def generate_response(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None) -> Any:
        metrics.total_requests += 1
        
        # Deterministic routing:
        # If there are NO tools requested AND this isn't a tool follow-up, the query is simple factual/conversational -> Local (Ollama)
        # If tools are requested OR it's a tool result summary -> Complex/Action-oriented -> Cloud (Groq)
        
        has_tool_messages = any(m.get("role") == "tool" for m in messages)
        use_local = (not tools or len(tools) == 0) and not has_tool_messages
        
        if use_local:
            logger.info("Hybrid Router: Routing to OLLAMA (Local) for simple request")
            metrics.ollama_requests += 1
            if self.ollama.test_connection():
                try:
                    response = self.ollama.generate_response(messages, tools)
                    metrics.ollama_successes += 1
                    return response
                except Exception as e:
                    logger.warning(f"Ollama failed during generation: {e}. Falling back to Groq.")
            else:
                logger.warning("Ollama connection test failed. Falling back to Groq.")
        
        # Fallback or Tool routing -> Groq
        logger.info("Hybrid Router: Routing to GROQ (Cloud) for complex/tool request")
        metrics.groq_requests += 1
        try:
            response = self.groq.generate_response(messages, tools)
            metrics.groq_successes += 1
            return response
        except Exception as e:
            # Re-raise Groq exceptions (like rate limits) up to the AI Engine
            raise e
            
    def test_connection(self) -> bool:
        # Hybrid is considered healthy if at least one is healthy (primarily Groq as fallback)
        return self.groq.test_connection()
