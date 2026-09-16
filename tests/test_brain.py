import pytest
from unittest.mock import MagicMock, patch
from app.brain.llm import AIEngine
from app.core.exceptions import AIError

@patch("app.brain.providers.get_provider")
def test_generate_response_empty(mock_get_provider):
    ai = AIEngine()
    result = ai.generate_response("")
    assert result == ""
    assert len(ai.memory.get_messages()) == 0

@patch("app.brain.providers.get_provider")
def test_generate_response_success(mock_get_provider):
    mock_provider = MagicMock()
    mock_get_provider.return_value = mock_provider
    
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "I am JARVIS."
    mock_response.choices[0].message.tool_calls = None
    
    mock_provider.generate_response.return_value = mock_response
    
    ai = AIEngine()
    
    result = ai.generate_response("Who are you?")
    assert result == "I am JARVIS."
    mock_provider.generate_response.assert_called_once()
    
    # Verify memory
    messages = ai.memory.get_messages()
    assert len(messages) == 2
    assert messages[0] == {"role": "user", "content": "Who are you?"}
    assert messages[1] == {"role": "assistant", "content": "I am JARVIS."}
    
    # Second turn
    mock_response.choices[0].message.content = "I was created by you."
    result2 = ai.generate_response("Who created you?")
    
    messages_second_call = mock_provider.generate_response.call_args[1]["messages"]
    assert len(messages_second_call) == 4
    
    # Verify the system prompt is included and separate from history
    system_message = messages_second_call[0]
    assert system_message["role"] == "system"
    # Verify personality instructions are in the system prompt
    assert "calm, professional" in system_message["content"]
    assert "personal desktop AI assistant" in system_message["content"]
    
    assert messages_second_call[1]["role"] == "user"
    assert messages_second_call[1]["content"] == "Who are you?"
    assert messages_second_call[2]["role"] == "assistant"
    assert messages_second_call[2]["content"] == "I am JARVIS."
    assert messages_second_call[3]["role"] == "user"
    assert messages_second_call[3]["content"] == "Who created you?"

@patch("app.brain.providers.get_provider")
def test_generate_response_failure(mock_get_provider):
    mock_provider = MagicMock()
    mock_get_provider.return_value = mock_provider
    mock_provider.generate_response.side_effect = Exception("API Error")
    
    ai = AIEngine()
    
    with pytest.raises(AIError):
        ai.generate_response("Will this break memory?")
        
    assert len(ai.memory.get_messages()) == 0
