from typing import List, Dict
from app.core.config import settings
from app.core.logger import logger

class ShortTermMemory:
    def __init__(self, max_messages: int = settings.MAX_HISTORY_MESSAGES):
        self.max_messages = max_messages
        self.history: List[Dict[str, str]] = []

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the memory and truncate if it exceeds max_messages."""
        if not content:
            return
            
        self.history.append({"role": role, "content": content})
        
        # Keep only the last max_messages
        if len(self.history) > self.max_messages:
            self.history = self.history[-self.max_messages:]
            logger.debug("Conversation memory truncated to stay within limits.")

    def get_messages(self) -> List[Dict[str, str]]:
        """Return the current conversation history."""
        return self.history.copy()

    def clear(self) -> None:
        """Clear the conversation memory."""
        self.history.clear()
        logger.info("Conversation memory cleared.")
