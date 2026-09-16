import pytest
from app.voice.asr import SpeechRecognizer

def test_validate_transcription():
    asr = SpeechRecognizer()
    
    # Empty
    assert asr.validate_transcription("") == ""
    
    # Extremely short
    assert asr.validate_transcription("a") == ""
    assert asr.validate_transcription("ok") == "ok"
    assert asr.validate_transcription("a.") == ""
    
    # Normal short word
    assert asr.validate_transcription("yes") == "yes"
    assert asr.validate_transcription("no") == "no"
    
    # Meaningless noise words
    assert asr.validate_transcription("um") == ""
    assert asr.validate_transcription("uh-huh") == ""
    assert asr.validate_transcription("hmm.") == ""
    assert asr.validate_transcription("Oh") == ""
    assert asr.validate_transcription("Okay.") == ""
    
    # Normal commands
    assert asr.validate_transcription("What is Python?") == "What is Python?"
    assert asr.validate_transcription("search google") == "search google"
