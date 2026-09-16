from typing import List, Dict, Any, Optional
import requests
import json
from app.core.config import settings
from app.core.logger import logger
from app.core.exceptions import AIError
from app.brain.providers.base import BaseLLMProvider

# We need to construct a mock OpenAI message structure to maintain compatibility
# with the existing AIEngine code that expects response.choices[0].message
class MockToolCallFunction:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

class MockToolCall:
    def __init__(self, id, name, arguments):
        self.id = id
        self.function = MockToolCallFunction(name, arguments)
        self.type = "function"

class MockMessage:
    def __init__(self, content, tool_calls=None):
        self.content = content
        self.tool_calls = tool_calls
        self.role = "assistant"
        
    def model_dump(self, exclude_none=True):
        res = {"role": self.role}
        if self.content:
            res["content"] = self.content
        if self.tool_calls:
            res["tool_calls"] = []
            for tc in self.tool_calls:
                res["tool_calls"].append({
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                })
        return res

class MockChoice:
    def __init__(self, message):
        self.message = message

class MockResponse:
    def __init__(self, message):
        self.choices = [MockChoice(message)]

class OllamaProvider(BaseLLMProvider):
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL.rstrip('/')
        self.model = settings.OLLAMA_MODEL

    def test_connection(self) -> bool:
        try:
            res = requests.get(f"{self.base_url}/api/tags", timeout=3)
            if res.status_code == 200:
                models = [m["name"] for m in res.json().get("models", [])]
                if any(m.startswith(self.model) for m in models):
                    return True
                logger.warning(f"Ollama connected, but model {self.model} not found.")
                return False
            return False
        except Exception as e:
            logger.warning(f"Ollama connection failed: {e}")
            return False

    def generate_response(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None) -> Any:
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.7
            }
        }
        
        if tools:
            # Ollama expects tools in a slightly different format, but recent versions support OpenAI format directly
            payload["tools"] = tools

        try:
            logger.debug(f"Sending request to Ollama ({self.model})")
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            message_data = data.get("message", {})
            content = message_data.get("content", "")
            
            # Parse tool calls
            tool_calls_data = message_data.get("tool_calls", [])
            tool_calls = None
            
            if tool_calls_data:
                tool_calls = []
                import uuid
                for tc in tool_calls_data:
                    func = tc.get("function", {})
                    name = func.get("name", "")
                    # Ollama sometimes returns a dict, sometimes a string for arguments
                    args = func.get("arguments", {})
                    if isinstance(args, dict):
                        args = json.dumps(args)
                        
                    tc_id = f"call_{uuid.uuid4().hex[:8]}"
                    tool_calls.append(MockToolCall(tc_id, name, args))
                    
            mock_msg = MockMessage(content, tool_calls)
            return MockResponse(mock_msg)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama request failed: {e}")
            raise AIError(f"Local AI failed to generate response: {e}")
        except Exception as e:
            logger.error(f"Unexpected Ollama error: {e}")
            raise AIError(f"Local AI error: {e}")
