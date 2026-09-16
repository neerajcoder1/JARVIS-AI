import json
import os
from pathlib import Path
from typing import List
from app.memory.models import MemoryItem
from app.core.logger import logger

class MemoryStore:
    def __init__(self, file_path: str = ".jarvis/long_term_memory.json"):
        self.file_path = Path(file_path)
        self._ensure_file()

    def _ensure_file(self) -> None:
        if not self.file_path.parent.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.write_text(json.dumps([]))

    def get_all(self) -> List[MemoryItem]:
        try:
            data = json.loads(self.file_path.read_text())
            return [MemoryItem(**item) for item in data]
        except Exception as e:
            logger.error(f"Failed to load memory file: {e}")
            return []

    def save_all(self, items: List[MemoryItem]) -> None:
        try:
            self.file_path.write_text(json.dumps([item.model_dump(mode="json") for item in items], indent=2))
        except Exception as e:
            logger.error(f"Failed to save memory file: {e}")
            raise e
