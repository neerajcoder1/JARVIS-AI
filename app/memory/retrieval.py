from typing import List, Optional
from app.memory.store import MemoryStore
from app.memory.models import MemoryItem

class MemoryRetrieval:
    def __init__(self, store: MemoryStore = None):
        self.store = store or MemoryStore()

    def search(self, query: Optional[str] = None, category: Optional[str] = None) -> List[MemoryItem]:
        items = self.store.get_all()
        results = items
        
        if category:
            results = [item for item in results if item.category == category]
            
        if query:
            q_lower = query.lower()
            results = [item for item in results if q_lower in item.content.lower()]
            
        return results
