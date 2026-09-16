# JARVIS v1.0

JARVIS is a completely local-first, voice-activated AI desktop assistant for Windows. It utilizes continuous listening, seamless language switching (English/Hindi/Hinglish), and hybrid LLM routing (Groq for complex logic, Ollama for local fallback) to provide a powerful hands-free desktop experience.

## Requirements
- OS: Windows 10/11
- Python: 3.12+
- Audio: Working Microphone & Speakers
- Tools: Chrome (for web scraping), Tesseract (for screen OCR, optional)
- Ollama: Installed and running locally (if using local fallback)

## Installation
See `SETUP.md` for detailed installation instructions.

## Configuration
See `.env.example`. You will need to configure `GROQ_API_KEY` for cloud reasoning and set your local filesystem sandbox paths.

## Running JARVIS
Activate the virtual environment and run:
```bash
python run.py
```
JARVIS will calibrate ambient noise and begin continuous background listening.

## Supported Voice Interaction
- Completely hands-free continuous listening (no wake word needed).
- Automatically filters out ambient noise and short accidental utterances.
- Dynamically interrupts TTS playback if you speak over it.
- Seamlessly understands and responds in English, Hindi, and Hinglish.

## Local LLM vs Cloud (Hybrid Routing)
JARVIS routes simple conversational and factual tasks to a local Ollama instance (default: `llama3.2`), and complex reasoning or tool-planning tasks to Groq (`llama3-70b-8192`). 

## Windows Auto Start
You can configure JARVIS to launch automatically when you log into Windows. This runs under your current user session and does not require administrator privileges.

To install the startup script:
```bash
python setup_startup.py
```
To check if it's currently enabled:
```bash
python setup_startup.py --status
```
To disable auto start:
```bash
python setup_startup.py --disable
```

## Tools
- Application Control (Open/Close allowed apps)
- Web Browser Automation (Open URL, Get Title, Read Text, Click Links)
- Filesystem (List, Read, Find, Create, Copy, Delete within a strict Sandbox)
- Input Automation (Mouse Move/Click, Keyboard Type/Press - strictly sandboxed)
- Screen Understanding (Local OCR, no pixels uploaded)
- Long-Term Memory (Persistent JSON store)
- Safe Power Control ("Shutdown my laptop", "Restart my laptop", "Put my laptop to sleep", "Log me out" - explicitly requiring CONFIRM permission)

## Security Model
JARVIS adheres to a strict privilege model (`SAFE`, `CONFIRM`, `RESTRICTED`). See `SECURITY.md` for details on prompt injection protections, credential scrubbing, and sandbox paths.

## Limitations
- Continuous listening may falsely trigger if media (YouTube, movies) is playing out loud.
- Tesseract OCR for screen reading struggles with non-standard fonts.
- Filesystem writes are explicitly restricted to predefined sandbox directories.
