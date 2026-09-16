import pytest
from app.brain.llm import AIEngine
from unittest.mock import patch, MagicMock

class MockResponse:
    def __init__(self, content):
        self.choices = [MagicMock(message=MagicMock(content=content, tool_calls=None))]
        self.choices[0].message.model_dump.return_value = {"role": "assistant", "content": content}

@pytest.fixture
def ai_engine():
    # We patch OpenAI so it doesn't make real API calls in simple unittests
    # But wait, this is a regression test, maybe the user wants real API calls to test the prompt?
    # The prompt explicitly says: "Do not make tests depend on exact wording unless necessary. Test semantic properties where practical."
    # If I mock the response, I'm testing the test. The user probably wants real LLM tests if it's checking the prompt's effectiveness.
    pass
