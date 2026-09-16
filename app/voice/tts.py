from app.core.config import settings
from app.core.logger import logger
from app.core.exceptions import TTSError

class SpeechSynthesizer:
    def __init__(self):
        try:
            self.provider_name = settings.TTS_PROVIDER.lower()
            
            if self.provider_name == "edge":
                from app.voice.providers.edge_tts_provider import EdgeTTSProvider
                self.provider = EdgeTTSProvider(voice=settings.TTS_VOICE)
            else:
                logger.warning(f"Unknown TTS_PROVIDER '{self.provider_name}'. Falling back to EdgeTTSProvider.")
                from app.voice.providers.edge_tts_provider import EdgeTTSProvider
                self.provider = EdgeTTSProvider(voice="en-US-AriaNeural")
                
        except Exception as e:
            logger.error(f"[ERROR] TTS failure: {e}")
            raise TTSError(f"TTS initialization failed: {e}")

    def speak(self, text: str, interrupt_event=None) -> None:
        if not text:
            return
            
        try:
            import re
            # Default to current provider voice
            current_voice = self.provider.voice if hasattr(self.provider, "voice") else None
            
            # Extract [LANG:HI] or [LANG:EN]
            match = re.search(r'\[LANG:(HI|EN)\]', text, re.IGNORECASE)
            if match:
                lang = match.group(1).upper()
                text = re.sub(r'\[LANG:(HI|EN)\]', '', text, flags=re.IGNORECASE).strip()
                
                if lang == "HI" and hasattr(self.provider, "voice"):
                    # Use a Hindi capable voice for this utterance
                    # hi-IN-SwaraNeural is great for Hindi & Hinglish
                    current_voice = "hi-IN-SwaraNeural"
                    
            if hasattr(self.provider, "voice"):
                original_voice = self.provider.voice
                self.provider.voice = current_voice
                self.provider.synthesize_and_play(text, interrupt_event=interrupt_event)
                self.provider.voice = original_voice
            else:
                self.provider.synthesize_and_play(text, interrupt_event=interrupt_event)
                
            logger.info("TTS completed")
        except Exception as e:
            logger.error(f"[ERROR] TTS failure: {e}")
