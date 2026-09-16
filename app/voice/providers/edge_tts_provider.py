import asyncio
import os
import tempfile
import pygame
import edge_tts
from app.core.logger import logger
from app.voice.providers.base import TTSProvider

class EdgeTTSProvider(TTSProvider):
    def __init__(self, voice: str):
        self.voice = voice
        try:
            pygame.mixer.init()
        except Exception as e:
            logger.error(f"[ERROR] TTS failure: Failed to initialize pygame mixer: {e}")

    def synthesize_and_play(self, text: str, interrupt_event=None) -> None:
        if not text:
            return

        try:
            # Create a temporary file to hold the MP3
            temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            temp_path = temp_file.name
            temp_file.close()

            # Generate audio synchronously using asyncio
            async def _generate():
                communicate = edge_tts.Communicate(text, self.voice)
                await communicate.save(temp_path)

            asyncio.run(_generate())

            # Play the generated audio and block until complete
            logger.info("Speaking...")
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                if interrupt_event and interrupt_event.is_set():
                    logger.info("TTS interrupted!")
                    pygame.mixer.music.stop()
                    break
                pygame.time.Clock().tick(10)

        except Exception as e:
            logger.error(f"[ERROR] TTS failure: {e}")
        finally:
            # Clean up audio resources to prevent locking
            try:
                pygame.mixer.music.unload()
            except Exception:
                pass
            
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except Exception as e:
                logger.error(f"[ERROR] TTS failure: Failed to remove temporary audio file: {e}")
