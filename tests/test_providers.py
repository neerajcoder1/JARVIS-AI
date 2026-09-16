import pytest
from unittest.mock import patch, MagicMock
from app.brain.providers.groq_provider import GroqProvider
from app.brain.providers.ollama_provider import OllamaProvider
from app.brain.providers import get_provider
from app.core.exceptions import AIError, AIRateLimitError

def test_get_provider_groq(monkeypatch):
    monkeypatch.setattr("app.core.config.settings.LLM_PROVIDER", "groq")
    provider = get_provider()
    assert isinstance(provider, GroqProvider)

def test_get_provider_ollama(monkeypatch):
    monkeypatch.setattr("app.core.config.settings.LLM_PROVIDER", "ollama")
    provider = get_provider()
    assert isinstance(provider, OllamaProvider)

@patch("app.brain.providers.groq_provider.OpenAI")
def test_groq_generate_response(MockOpenAI):
    mock_client = MockOpenAI.return_value
    mock_client.chat.completions.create.return_value = "mock_response"
    
    provider = GroqProvider()
    res = provider.generate_response([{"role": "user", "content": "hello"}])
    assert res == "mock_response"

@patch("app.brain.providers.ollama_provider.requests")
def test_ollama_generate_response(mock_requests):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "message": {
            "content": "local response",
            "tool_calls": []
        }
    }
    mock_requests.post.return_value = mock_response
    
    provider = OllamaProvider()
    res = provider.generate_response([{"role": "user", "content": "hello"}])
    assert res.choices[0].message.content == "local response"

@patch("app.brain.providers.ollama_provider.requests")
def test_ollama_connection_fails(mock_requests):
    mock_requests.get.side_effect = Exception("Connection refused")
    provider = OllamaProvider()
    assert provider.test_connection() == False

@patch("app.brain.providers.ollama_provider.requests")
def test_ollama_connection_success(mock_requests):
    mock_response = MagicMock()
    mock_response.status_code = 200
    # Simulate our model is phi3:mini
    mock_response.json.return_value = {"models": [{"name": "phi3:mini"}]}
    mock_requests.get.return_value = mock_response
    
    provider = OllamaProvider()
    provider.model = "phi3"
    assert provider.test_connection() == True
