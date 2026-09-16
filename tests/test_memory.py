import pytest
from app.brain.memory import ShortTermMemory
from app.core.config import settings

def test_add_message():
    memory = ShortTermMemory(max_messages=5)
    memory.add_message("user", "Hello")
    messages = memory.get_messages()
    assert len(messages) == 1
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Hello"

def test_add_empty_message():
    memory = ShortTermMemory()
    memory.add_message("user", "")
    assert len(memory.get_messages()) == 0

def test_history_limit():
    memory = ShortTermMemory(max_messages=3)
    memory.add_message("user", "Msg 1")
    memory.add_message("assistant", "Msg 2")
    memory.add_message("user", "Msg 3")
    memory.add_message("assistant", "Msg 4")
    
    messages = memory.get_messages()
    assert len(messages) == 3
    assert messages[0]["content"] == "Msg 2"
    assert messages[2]["content"] == "Msg 4"

def test_clear_memory():
    memory = ShortTermMemory()
    memory.add_message("user", "Hello")
    assert len(memory.get_messages()) == 1
    memory.clear()
    assert len(memory.get_messages()) == 0
