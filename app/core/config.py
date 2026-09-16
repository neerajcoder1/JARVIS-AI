from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    OPENAI_API_KEY: Optional[str] = None
    LLM_PROVIDER: str = "hybrid"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "phi3:mini"
    JARVIS_NAME: str = "JARVIS"
    LOG_LEVEL: str = "INFO"
    WAKE_WORD: str = "JARVIS"
    
    TTS_PROVIDER: str = "edge"
    TTS_VOICE: str = "en-US-AriaNeural"
    TTS_MODEL: str = "default"
    
    MAX_HISTORY_MESSAGES: int = 20
    ACTIVE_SESSION_TIMEOUT_SECONDS: int = 10
    
    # Filesystem Configuration
    FILESYSTEM_ALLOWED_ROOTS: str = "" # Comma-separated paths
    FILESYSTEM_MAX_LIST_ITEMS: int = 100
    FILESYSTEM_MAX_SEARCH_RESULTS: int = 100
    FILESYSTEM_MAX_SEARCH_DEPTH: int = 5
    FILESYSTEM_MAX_READ_BYTES: int = 1048576 # 1 MB

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
