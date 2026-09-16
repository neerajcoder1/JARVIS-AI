# Changelog

## [1.0.0] - 2026-09-16

### Added
- **Hybrid LLM Provider:** Intelligent routing between Groq (Cloud) and Ollama (Local) to optimize API usage and privacy.
- **Multilingual Support:** Seamless transition between English, Hindi, and Hinglish for ASR and TTS (`EdgeTTSProvider`).
- **Continuous Listening:** Zero-latency background microphone polling with intelligent noise filtering and playback interruption.
- **Controlled Screen Understanding:** Local OCR integration (`pytesseract`) allowing JARVIS to read visible screen elements without uploading pixels.
- **Mouse & Keyboard Control:** Precision UI automation tools bound to explicit user confirmation barriers.
- **Long-Term Memory:** Contextual `MemoryManager` with categorized storage (`user_preferences`, `project_information`) injected automatically into the system prompt.
- **Filesystem Sandbox:** Strict bounds for file creation, modification, and deletion. 
- **Security Enhancements:** Prompt-injection framing applied to external file reading and web browsing; credential and API key scrubbing in memory states.

### Fixed
- Fixed audio feedback loop where TTS playback would trigger the microphone.
- Fixed rate-limit exhaustion by shunting simplistic queries to local models.
- Blocked arbitrary command execution by standardizing application control onto an explicit allowlist.
