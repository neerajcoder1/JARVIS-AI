import sys
from unittest.mock import patch, MagicMock
from app.core.exceptions import AudioTimeoutError

@patch("run.WakeWordDetector")
@patch("run.SpeechRecognizer")
@patch("run.AIEngine")
@patch("run.SpeechSynthesizer")
def simulate_tool_flow(MockTTS, MockAI, MockASR, MockWake):
    from run import start_voice_loop
    
    # We want to test the LLM actual behavior, so we don't mock AIEngine!
    # Let's unpatch AIEngine
    pass

if __name__ == "__main__":
    pass
