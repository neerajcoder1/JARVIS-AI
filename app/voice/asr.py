import speech_recognition as sr
from app.core.config import settings
from app.core.logger import logger
from app.core.exceptions import AudioError, ASRError, AudioTimeoutError

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self, timeout: int = settings.ACTIVE_SESSION_TIMEOUT_SECONDS) -> sr.AudioData:
        """Listen to the microphone and return audio data"""
        try:
            with sr.Microphone() as source:
                logger.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info("Listening for command...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=15)
                return audio
        except sr.WaitTimeoutError:
            raise AudioTimeoutError("No audio detected within timeout.")
        except Exception as e:
            raise AudioError(f"Microphone error: {e}")

    def validate_transcription(self, text: str) -> str:
        """Filter out empty, extremely short, or meaningless noise."""
        if not text:
            return ""
            
        import re
        cleaned = re.sub(r'[^\w\s]', '', text).strip()
        
        # Extremely short audio is usually just throat clearing, sighs, etc.
        # But 'no', 'ok', 'hi' are valid 2-letter words.
        if len(cleaned) <= 1:
            logger.info(f"Ignoring meaningless extremely short transcription: '{text}'")
            return ""
            
        # Common ambient noise interpretations
        noise_words = {"um", "uh", "ah", "hmm", "huh", "oh", "okay", "yeah", "hmm", "uhhuh"}
        if cleaned.lower() in noise_words:
            logger.info(f"Ignoring background filler noise: '{text}'")
            return ""
            
        return text.strip()

    def transcribe(self, audio: sr.AudioData) -> str:
        """Transcribe audio data to text"""
        if not audio:
            raise ASRError("No audio data provided")
            
        try:
            logger.info("Speech detected")
            text = self.recognizer.recognize_google(audio, language="hi-IN")
            logger.info(f"Transcription: {text}")
            return self.validate_transcription(text)
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return ""
        except sr.RequestError as e:
            logger.error(f"Could not request results from ASR service; {e}")
            raise ASRError("ASR service unavailable")
        except Exception as e:
            logger.error(f"ASR error: {e}")
            raise ASRError(f"Transcription failed: {e}")

    def listen_and_transcribe(self) -> str:
        """Convenience method to listen and transcribe"""
        audio = self.listen()
        return self.transcribe(audio)
