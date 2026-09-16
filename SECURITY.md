# JARVIS Security Model

JARVIS implements rigorous security boundaries to prevent prompt injections, arbitrary execution, and destructive behaviors. 

## Permission Levels
All tools use a strict schema definition and require one of the following permission levels:
- `SAFE`: Tool runs automatically (e.g., getting system time, reading a file).
- `CONFIRM`: Requires explicit user confirmation via voice or terminal before execution (e.g., writing files, sending mouse clicks).
- `RESTRICTED`: High-risk actions that demand confirmation and cannot be executed automatically under any circumstance (e.g., file deletion).

## Untrusted Data Boundaries
- **Indirect Prompt Injection:** Any data read from the filesystem (`FilesystemReadTextTool`) or the web (`BrowserReadPageTool`) is explicitly bracketed with trust markers (e.g., `--- WEBPAGE CONTENT START ---`). The LLM is actively instructed to treat this data as untrusted and not execute instructions found within it.

## System Defenses
- **Arbitrary Command Execution:** No raw shell or PowerShell execution tools exist. Application control is bound to a hardcoded `ALLOWLIST` mapping safe applications (e.g., 'notepad', 'chrome') directly to their executables with `shell=False`.
- **Path Traversal:** File system access is forcibly routed through `sandbox.py` using absolute `Path.resolve()`, enforcing operations only occur within user-designated `.env` root directories.
- **Sensitive Data Scrubbing:** `MemoryManager` runs regex scrubbing to actively catch and reject the persistence of API keys, Bearer tokens, or passwords.
- **Screen Reading Privacy:** The screen understanding tool relies purely on local `pytesseract` OCR. Pixel data is immediately discarded and NEVER uploaded to a cloud provider.
