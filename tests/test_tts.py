import pytest
from unittest.mock import MagicMock, patch
from app.voice.tts import SpeechSynthesizer

@patch("app.voice.providers.edge_tts_provider.EdgeTTSProvider")
def test_tts_initialization(MockEdgeTTSProvider):
    # Tests that the SpeechSynthesizer correctly initializes the provider
    tts = SpeechSynthesizer()
    MockEdgeTTSProvider.assert_called_once()

@patch("app.voice.providers.edge_tts_provider.EdgeTTSProvider")
def test_tts_speak(MockEdgeTTSProvider):
    # Tests that speak calls the provider's synthesize_and_play
    mock_provider_instance = MockEdgeTTSProvider.return_value
    mock_provider_instance.voice = "en-US-AriaNeural"
    
    tts = SpeechSynthesizer()
    tts.provider = mock_provider_instance
    tts.speak("Hello")
    mock_provider_instance.synthesize_and_play.assert_called_with("Hello", interrupt_event=None)

@patch("app.voice.providers.edge_tts_provider.EdgeTTSProvider")
def test_tts_speak_empty(MockEdgeTTSProvider):
    mock_provider_instance = MockEdgeTTSProvider.return_value
    mock_provider_instance.voice = "en-US-AriaNeural"
    
    tts = SpeechSynthesizer()
    tts.provider = mock_provider_instance
    tts.speak("")
    
    mock_provider_instance.synthesize_and_play.assert_not_called()

@patch("app.voice.providers.edge_tts_provider.EdgeTTSProvider")
def test_tts_multilingual_english(MockEdgeTTSProvider):
    mock_provider_instance = MockEdgeTTSProvider.return_value
    mock_provider_instance.voice = "en-US-AriaNeural"
    
    tts = SpeechSynthesizer()
    tts.provider = mock_provider_instance
    tts.speak("[LANG:EN] Hello world")
    
    mock_provider_instance.synthesize_and_play.assert_called_with("Hello world", interrupt_event=None)
    assert mock_provider_instance.voice == "en-US-AriaNeural"  # Restores default

@patch("app.voice.providers.edge_tts_provider.EdgeTTSProvider")
def test_tts_multilingual_hindi(MockEdgeTTSProvider):
    mock_provider_instance = MockEdgeTTSProvider.return_value
    mock_provider_instance.voice = "en-US-AriaNeural"
    
    tts = SpeechSynthesizer()
    tts.provider = mock_provider_instance
    tts.speak("[LANG:HI] Python kya hai")
    
    mock_provider_instance.synthesize_and_play.assert_called_with("Python kya hai", interrupt_event=None)
    assert mock_provider_instance.voice == "en-US-AriaNeural"
