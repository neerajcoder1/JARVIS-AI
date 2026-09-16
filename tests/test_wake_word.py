import pytest
from unittest.mock import patch
from app.voice.wake_word import WakeWordDetector

@pytest.fixture
def detector():
    with patch("app.voice.wake_word.Model"):
        return WakeWordDetector("jarvis")

def test_extract_command_exact(detector):
    command = detector.extract_command("JARVIS")
    assert command == ""

def test_extract_command_with_text(detector):
    command = detector.extract_command("JARVIS, what is Python?")
    assert command == "what is python?"

def test_extract_command_with_prefix(detector):
    command = detector.extract_command("Hey JARVIS, what is Python?")
    assert command == "what is python?"

def test_extract_command_case_insensitive(detector):
    command = detector.extract_command("jarvis tell me the time")
    assert command == "tell me the time"

def test_extract_command_no_wake_word(detector):
    command = detector.extract_command("what is cybersecurity")
    assert command is None

def test_extract_command_empty(detector):
    assert detector.extract_command("") is None
    assert detector.extract_command(None) is None
