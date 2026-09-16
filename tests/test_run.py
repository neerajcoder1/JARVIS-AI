import pytest
import queue
from unittest.mock import patch, MagicMock
from app.core.exceptions import AudioTimeoutError

@patch("time.sleep")
@patch("run.SpeechRecognizer")
@patch("run.AIEngine")
@patch("run.SpeechSynthesizer")
@patch("run.sr.Microphone")
@patch("queue.Queue.get")
def test_voice_loop_continuous(MockGet, MockMic, MockTTS, MockAI, MockASR, MockSleep):
    from run import start_voice_loop
    
    mock_tts = MockTTS.return_value
    mock_asr = MockASR.return_value
    mock_ai = MockAI.return_value
    
    # Simulate first turn valid command, second turn KeyboardInterrupt
    MockGet.side_effect = ["What is Python?", KeyboardInterrupt()]
    mock_ai.generate_response.return_value = "Python is a language."
    
    start_voice_loop()
    
    # Verify Startup Greeting
    mock_tts.speak.assert_any_call("Welcome Neeraj Sir. I am your JARVIS assistant.")
    # Verify grace period sleep
    MockSleep.assert_any_call(2)
    
    mock_ai.generate_response.assert_called_with("What is Python?")
    # Check that TTS was called with the response and the interrupt event
    args, kwargs = mock_tts.speak.call_args
    assert args[0] == "Python is a language."
    assert "interrupt_event" in kwargs

@patch("time.sleep")
@patch("run.SpeechRecognizer")
@patch("run.AIEngine")
@patch("run.SpeechSynthesizer")
@patch("run.sr.Microphone")
@patch("queue.Queue.get")
def test_voice_loop_timeout_recovers(MockGet, MockMic, MockTTS, MockAI, MockASR, MockSleep):
    from run import start_voice_loop
    
    mock_tts = MockTTS.return_value
    mock_asr = MockASR.return_value
    mock_ai = MockAI.return_value
    
    # turn 1: queue.Empty (timeout equivalent)
    # turn 2: valid command
    # turn 3: "exit"
    MockGet.side_effect = [
        queue.Empty(),
        "what is cybersecurity", 
        "exit"
    ]
    
    mock_ai.generate_response.return_value = "Cybersecurity is..."
    
    start_voice_loop()
    
    # AI generated response once for the valid turn
    assert mock_ai.generate_response.call_count == 1
    
    # Exited gracefully
    args, kwargs = mock_tts.speak.call_args
    assert args[0] == "Goodbye."
