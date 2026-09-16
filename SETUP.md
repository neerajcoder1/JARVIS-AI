# JARVIS Setup Guide

## 1. Prerequisites
- **Python 3.12+**
- **Windows OS**
- **Ollama** (Download from [ollama.com](https://ollama.com) for local AI)
- **Tesseract-OCR** (Optional, for screen understanding tool)

## 2. Environment Setup
1. Clone the repository and navigate to it:
   ```bash
   cd JARVIS
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 3. Configuration
1. Copy the example configuration:
   ```bash
   cp .env.example .env
   ```
2. Add your **Groq API Key**:
   ```env
   GROQ_API_KEY=gsk_your_key_here
   ```
3. (Optional) Set up your Sandbox boundaries. Define allowed directories for file manipulation:
   ```env
   FILESYSTEM_ALLOWED_ROOTS=C:\Users\YourName\Desktop,C:\Users\YourName\Documents
   ```

## 4. Run JARVIS
```bash
python run.py
```
