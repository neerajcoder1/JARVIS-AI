from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    @abstractmethod
    def generate_response(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None) -> Any:
        """
        Generates a response from the LLM provider.
        Should return an object that mimics the OpenAI response format:
        response.choices[0].message (with content, tool_calls, etc.)
        """
        pass

    @abstractmethod
    def test_connection(self) -> bool:
        """
        Tests if the provider is healthy and reachable.
        """
        pass
