import pytest
from unittest.mock import MagicMock, patch
from app.voice.asr import SpeechRecognizer
from app.core.exceptions import ASRError, AudioError
import speech_recognition as sr

def test_transcribe_empty_audio():
    recognizer = SpeechRecognizer()
    with pytest.raises(ASRError):
        recognizer.transcribe(None)

@patch("speech_recognition.Recognizer.recognize_google")
def test_transcribe_success(mock_recognize):
    mock_recognize.return_value = "hello jarvis"
    recognizer = SpeechRecognizer()
    audio_mock = MagicMock(spec=sr.AudioData)
    
    result = recognizer.transcribe(audio_mock)
    assert result == "hello jarvis"

@patch("speech_recognition.Recognizer.recognize_google")
def test_transcribe_unknown_value(mock_recognize):
    mock_recognize.side_effect = sr.UnknownValueError()
    recognizer = SpeechRecognizer()
    audio_mock = MagicMock(spec=sr.AudioData)
    
    result = recognizer.transcribe(audio_mock)
    assert result == ""
