import threading
import uvicorn
import sys
import speech_recognition as sr
from app.main import app
from app.core.config import settings
from app.core.logger import logger
from app.voice.asr import SpeechRecognizer
from app.brain.llm import AIEngine
from app.voice.tts import SpeechSynthesizer
from app.core.exceptions import JarvisError, AudioTimeoutError

def start_api():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")

def start_voice_loop():
    logger.info("JARVIS started")
    
    try:
        asr = SpeechRecognizer()
        ai = AIEngine()
        tts = SpeechSynthesizer()
        
        # Register real computer tools for Phase 2A
        from app.tools.registry import registry
        from app.tools.applications import OpenApplicationTool, CloseApplicationTool
        from app.tools.system_info import GetSystemInfoTool
        from app.tools.time_tool import GetCurrentTimeTool
        from app.tools.browser import OpenWebsiteTool, SearchWebTool
        from app.tools.controlled_browser import BrowserOpenTool, BrowserGetPageTitleTool, BrowserReadPageTool, BrowserGetLinksTool, BrowserCloseTool
        from app.tools.filesystem import (
            FilesystemListTool, FilesystemReadTextTool, FilesystemFindTool, FilesystemGetMetadataTool,
            FilesystemCreateFileTool, FilesystemWriteTextTool, FilesystemAppendTextTool,
            FilesystemCreateDirectoryTool, FilesystemCopyTool, FilesystemMoveTool, FilesystemDeleteTool
        )
        
        from app.tools.memory_tools import SaveMemoryTool, RetrieveMemoryTool, DeleteMemoryTool, UpdateMemoryTool
        from app.tools.screen import InspectScreenTool
        from app.tools.input import MouseMoveTool, MouseClickTool, KeyboardTypeTool, KeyboardPressTool
        
        registry.register(OpenApplicationTool())
        registry.register(CloseApplicationTool())
        registry.register(GetSystemInfoTool())
        registry.register(GetCurrentTimeTool())
        registry.register(OpenWebsiteTool())
        registry.register(SearchWebTool())
        
        registry.register(BrowserOpenTool())
        registry.register(BrowserGetPageTitleTool())
        registry.register(BrowserReadPageTool())
        registry.register(BrowserGetLinksTool())
        registry.register(BrowserCloseTool())
        
        registry.register(FilesystemListTool())
        registry.register(FilesystemReadTextTool())
        registry.register(FilesystemFindTool())
        registry.register(FilesystemGetMetadataTool())
        registry.register(FilesystemCreateFileTool())
        registry.register(FilesystemWriteTextTool())
        registry.register(FilesystemAppendTextTool())
        registry.register(FilesystemCreateDirectoryTool())
        registry.register(FilesystemCopyTool())
        registry.register(FilesystemMoveTool())
        registry.register(FilesystemDeleteTool())
        
        registry.register(SaveMemoryTool())
        registry.register(RetrieveMemoryTool())
        registry.register(DeleteMemoryTool())
        registry.register(UpdateMemoryTool())
        
        registry.register(InspectScreenTool())
        
        registry.register(MouseMoveTool())
        registry.register(MouseClickTool())
        registry.register(KeyboardTypeTool())
        registry.register(KeyboardPressTool())
        
    except Exception as e:
        logger.error(f"Failed to initialize JARVIS components: {e}")
        return
    
    rate_limited = False
    import queue
    command_queue = queue.Queue()
    interruption_event = threading.Event()
    is_speaking = threading.Event()

    def asr_callback(recognizer, audio):
        if is_speaking.is_set():
            logger.info("Interruption detected during TTS!")
            interruption_event.set()
            return
            
        try:
            text = asr.transcribe(audio)
            if text:
                command_queue.put(text)
        except Exception as e:
            logger.debug(f"ASR background callback error: {e}")

    logger.info("Calibrating microphone and starting background listener...")
    import speech_recognition as sr
    source = sr.Microphone()
    with source:
        asr.recognizer.adjust_for_ambient_noise(source, duration=1)
    
    stop_listening = asr.recognizer.listen_in_background(source, asr_callback, phrase_time_limit=15)
    
    try:
        while True:
            if rate_limited:
                import time
                time.sleep(10)
                continue
            
            try:
                command = command_queue.get(timeout=1.0)
            except queue.Empty:
                continue
                
            if not command:
                continue
            
            # Check for exit command
            if command.lower() in ["exit", "quit", "stop", "goodbye"]:
                logger.info("Exit command received. Shutting down...")
                is_speaking.set()
                tts.speak("Goodbye.", interrupt_event=interruption_event)
                is_speaking.clear()
                break
            
            # Generate AI response
            response = ai.generate_response(command)
            if response:
                logger.info(f"{settings.JARVIS_NAME}: {response}")
                
                is_speaking.set()
                interruption_event.clear()
                
                # Speak response, allowing interruption
                tts.speak(response, interrupt_event=interruption_event)
                
                is_speaking.clear()
                interruption_event.clear()
                
                # Clear any queued commands generated from the echo of JARVIS
                while not command_queue.empty():
                    try:
                        command_queue.get_nowait()
                    except queue.Empty:
                        break
                    
    except getattr(__import__('app.core.exceptions', fromlist=['AIRateLimitError']), 'AIRateLimitError') as e:
        logger.error(str(e))
        is_speaking.set()
        tts.speak(str(e))
        is_speaking.clear()
        rate_limited = True
    except JarvisError as e:
        logger.error(str(e))
    except KeyboardInterrupt:
        logger.info("Interrupted by user. Shutting down...")
    except Exception as e:
        logger.error(f"Unexpected error in voice loop: {e}")
    finally:
        stop_listening(wait_for_stop=False)

if __name__ == "__main__":
    # Start FastAPI in a daemon thread
    api_thread = threading.Thread(target=start_api, daemon=True)
    api_thread.start()
    
    # Start main voice loop
    start_voice_loop()
    sys.exit(0)
