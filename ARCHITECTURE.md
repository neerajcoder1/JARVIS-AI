# JARVIS Architecture

JARVIS v1.0 utilizes a decoupled, asynchronous architecture suited for real-time continuous voice interaction and LLM tool orchestration.

## 1. Audio Processing Pipeline
- **Continuous Listener:** A daemon thread actively pulls frames from the microphone.
- **Voice Activity Detection (VAD):** Short bursts of noise (< 2 characters transcribed) are filtered locally via `validate_transcription`.
- **Transcription:** `SpeechRecognition` handles Google Web Speech API translation, seamlessly shifting between English, Hindi, and Hinglish.
- **Queueing:** Transcribed commands are pushed to a thread-safe `command_queue` to keep the audio thread unblocked.

## 2. LLM Engine & Routing
- **Hybrid Router:** Commands pass through NLP regex tiers. Simple factual or chat queries route to a **Local Ollama Model**. Queries implying tool usage (e.g., "create a file") route to **Groq (Llama-3-70b)**.
- **Memory Injection:** Short-term conversational history is passed alongside dynamically injected Long-Term Memory (preferences, project info) to create contextual awareness.

## 3. Tool Executor Layer
- **ToolRegistry:** Loads tools dynamically.
- **PermissionManager:** Checks tool schemas against the `SAFE` / `CONFIRM` / `RESTRICTED` security thresholds.
- **Execution:** Tools map Pydantic schema kwargs directly into deterministic Python logic.

## 4. Output Generation
- **Edge-TTS:** The resulting LLM response is analyzed for language tags (e.g., `[LANG:EN]` or `[LANG:HI]`). The Edge-TTS provider dynamically spins up the appropriate neural voice profile (`en-US-GuyNeural` or `hi-IN-SwaraNeural`) and plays it through `pygame.mixer`. 
- **Interruption Polling:** If the VAD thread detects speech *while* TTS is playing, it triggers an `interrupt_event`, killing TTS immediately to listen to the user.
