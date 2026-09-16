import json
import re
import pyaudio
from vosk import Model, KaldiRecognizer
from app.core.logger import logger
from app.core.config import settings

class WakeWordDetector:
    def __init__(self, wake_word: str = settings.WAKE_WORD):
        self.wake_word = wake_word.lower()
        logger.info("Initializing offline wake-word model...")
        try:
            self.model = Model(lang="en-us")
        except Exception as e:
            logger.error(f"Failed to load Vosk model: {e}")
            raise e

    def wait_for_wake_word(self) -> str:
        """
        Continuously listens offline using Vosk.
        Returns the extracted command when the wake word is detected.
        """
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, 
                        channels=1, 
                        rate=16000, 
                        input=True, 
                        frames_per_buffer=8000)
        stream.start_stream()
        
        rec = KaldiRecognizer(self.model, 16000)
        logger.info(f"Waiting for wake word '{self.wake_word}'...")
        
        try:
            while True:
                data = stream.read(4000, exception_on_overflow=False)
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "")
                    
                    if text and self.wake_word in text.lower():
                        # Extract command after wake word
                        command = self.extract_command(text)
                        
                        logger.info(f"Wake word detected! Extracted command: '{command}'")
                        return command
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

    def extract_command(self, text: str) -> str:
        """Helper for unit tests"""
        if not text:
            return None
            
        t_lower = text.lower()
        if self.wake_word in t_lower:
            parts = t_lower.split(self.wake_word, 1)
            command = parts[1].strip()
            return re.sub(r'^[,\s]+', '', command)
        return None
