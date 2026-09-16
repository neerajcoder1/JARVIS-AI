import pytest
from unittest.mock import patch, MagicMock
from app.brain.providers.hybrid_provider import HybridProvider, metrics

@pytest.fixture(autouse=True)
def reset_metrics():
    metrics.ollama_requests = 0
    metrics.groq_requests = 0
    metrics.total_requests = 0
    metrics.ollama_successes = 0
    metrics.groq_successes = 0

@patch("app.brain.providers.hybrid_provider.GroqProvider")
@patch("app.brain.providers.hybrid_provider.OllamaProvider")
def test_hybrid_routing_to_ollama(MockOllama, MockGroq):
    mock_ollama_instance = MockOllama.return_value
    mock_ollama_instance.test_connection.return_value = True
    mock_ollama_instance.generate_response.return_value = "local_response"
    
    mock_groq_instance = MockGroq.return_value
    
    provider = HybridProvider()
    
    # Empty tools list -> Local
    response = provider.generate_response([{"role": "user", "content": "What is Python?"}], tools=[])
    
    assert response == "local_response"
    mock_ollama_instance.generate_response.assert_called_once()
    mock_groq_instance.generate_response.assert_not_called()
    assert metrics.ollama_requests == 1
    assert metrics.groq_requests == 0

@patch("app.brain.providers.hybrid_provider.GroqProvider")
@patch("app.brain.providers.hybrid_provider.OllamaProvider")
def test_hybrid_routing_to_groq_with_tools(MockOllama, MockGroq):
    mock_ollama_instance = MockOllama.return_value
    mock_groq_instance = MockGroq.return_value
    mock_groq_instance.generate_response.return_value = "groq_response"
    
    provider = HybridProvider()
    
    # Non-empty tools list -> Groq
    response = provider.generate_response([{"role": "user", "content": "Open calculator"}], tools=[{"type": "function"}])
    
    assert response == "groq_response"
    mock_groq_instance.generate_response.assert_called_once()
    mock_ollama_instance.generate_response.assert_not_called()
    assert metrics.groq_requests == 1
    assert metrics.ollama_requests == 0

@patch("app.brain.providers.hybrid_provider.GroqProvider")
@patch("app.brain.providers.hybrid_provider.OllamaProvider")
def test_hybrid_routing_to_groq_with_tool_messages(MockOllama, MockGroq):
    mock_ollama_instance = MockOllama.return_value
    mock_groq_instance = MockGroq.return_value
    mock_groq_instance.generate_response.return_value = "groq_summary"
    
    provider = HybridProvider()
    
    # Tool summary (has tool role in history) -> Groq
    messages = [
        {"role": "assistant", "content": None, "tool_calls": [{"id": "1", "type": "function"}]},
        {"role": "tool", "content": "Success"}
    ]
    response = provider.generate_response(messages, tools=None)
    
    assert response == "groq_summary"
    mock_groq_instance.generate_response.assert_called_once()
    mock_ollama_instance.generate_response.assert_not_called()
    assert metrics.groq_requests == 1

@patch("app.brain.providers.hybrid_provider.GroqProvider")
@patch("app.brain.providers.hybrid_provider.OllamaProvider")
def test_hybrid_routing_ollama_fallback(MockOllama, MockGroq):
    mock_ollama_instance = MockOllama.return_value
    # Simulate connection failure
    mock_ollama_instance.test_connection.return_value = False
    
    mock_groq_instance = MockGroq.return_value
    mock_groq_instance.generate_response.return_value = "groq_fallback_response"
    
    provider = HybridProvider()
    
    # Wants local, but local is down -> Groq
    response = provider.generate_response([{"role": "user", "content": "What is Python?"}], tools=[])
    
    assert response == "groq_fallback_response"
    mock_groq_instance.generate_response.assert_called_once()
    assert metrics.ollama_requests == 1
    assert metrics.ollama_successes == 0
    assert metrics.groq_requests == 1

@patch("app.brain.providers.hybrid_provider.GroqProvider")
@patch("app.brain.providers.hybrid_provider.OllamaProvider")
def test_hybrid_routing_ollama_exception_fallback(MockOllama, MockGroq):
    mock_ollama_instance = MockOllama.return_value
    mock_ollama_instance.test_connection.return_value = True
    # Simulate exception during generation
    mock_ollama_instance.generate_response.side_effect = Exception("Ollama crashed")
    
    mock_groq_instance = MockGroq.return_value
    mock_groq_instance.generate_response.return_value = "groq_fallback_response2"
    
    provider = HybridProvider()
    
    # Wants local, local crashes -> Groq
    response = provider.generate_response([{"role": "user", "content": "What is Python?"}], tools=[])
    
    assert response == "groq_fallback_response2"
    mock_groq_instance.generate_response.assert_called_once()
    assert metrics.ollama_requests == 1
    assert metrics.ollama_successes == 0
    assert metrics.groq_requests == 1
