class JarvisError(Exception):
    """Base exception for JARVIS"""
    pass

class AudioError(JarvisError):
    """Raised when there is an issue with audio input/output"""
    pass

class AudioTimeoutError(AudioError):
    """Raised when audio times out due to inactivity"""
    pass

class ASRError(JarvisError):
    """Raised when Speech-to-Text fails"""
    pass

class TTSError(JarvisError):
    """Raised when Text-to-Speech fails"""
    pass

class AIError(JarvisError):
    """Raised when AI brain processing fails"""
    pass

class AIRateLimitError(AIError):
    """Raised when the LLM provider imposes a rate limit"""
    pass
