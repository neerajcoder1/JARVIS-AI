import sys
from unittest.mock import patch, MagicMock
from app.core.exceptions import AudioTimeoutError

@patch("run.WakeWordDetector")
@patch("run.SpeechRecognizer")
@patch("run.AIEngine")
@patch("run.SpeechSynthesizer")
def simulate_conversation(MockTTS, MockAI, MockASR, MockWake):
    from run import start_voice_loop
    
    mock_wake = MockWake.return_value
    mock_tts = MockTTS.return_value
    mock_asr = MockASR.return_value
    mock_ai = MockAI.return_value
    
    # 2. "JARVIS, what is Python?"
    # 6. "What is JavaScript?" (Ignored by wake word naturally since wait_for_wake_word blocks)
    # 7. "JARVIS, what is JavaScript?"
    # 8. "JARVIS", wait for Yes?, "What can you do?"
    mock_wake.wait_for_wake_word.side_effect = [
        "what is python",
        "what is javascript",
        "", # returns empty for just "JARVIS"
        "exit" # quit loop
    ]
    
    # Active conversation returns
    # Turn 2 -> "what is it used for"
    # Turn 3 -> "give me two examples"
    # Turn 4 -> Timeout
    # Turn 8 -> "what can you do"
    mock_asr.listen_and_transcribe.side_effect = [
        "what is it used for",
        "give me two examples",
        AudioTimeoutError(),
        "what can you do",
        AudioTimeoutError()
    ]
    
    mock_ai.generate_response.return_value = "Mocked AI Response."
    
    start_voice_loop()

if __name__ == "__main__":
    simulate_conversation()
