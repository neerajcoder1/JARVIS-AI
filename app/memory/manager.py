import uuid
from datetime import datetime, timezone
from app.memory.store import MemoryStore
from app.memory.models import MemoryItem
from app.memory.policies import validate_memory

class MemoryManager:
    def __init__(self, store: MemoryStore = None):
        self.store = store or MemoryStore()

    def save_memory(self, category: str, content: str) -> str:
        validate_memory(category, content)
        items = self.store.get_all()
        
        # Prevent exact duplicates
        for item in items:
            if item.category == category and item.content == content:
                raise ValueError("Duplicate memory already exists.")

        new_id = str(uuid.uuid4())
        new_item = MemoryItem(
            id=new_id,
            category=category,
            content=content,
            timestamp=datetime.now(timezone.utc)
        )
        items.append(new_item)
        self.store.save_all(items)
        return new_id

    def delete_memory(self, memory_id: str) -> bool:
        items = self.store.get_all()
        filtered = [item for item in items if item.id != memory_id]
        if len(filtered) == len(items):
            return False  # Not found
        self.store.save_all(filtered)
        return True

    def update_memory(self, memory_id: str, category: str, content: str) -> bool:
        validate_memory(category, content)
        items = self.store.get_all()
        for i, item in enumerate(items):
            if item.id == memory_id:
                items[i].category = category
                items[i].content = content
                items[i].timestamp = datetime.now(timezone.utc)
                self.store.save_all(items)
                return True
        return False
