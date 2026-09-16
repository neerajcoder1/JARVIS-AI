from pydantic import BaseModel, Field
from datetime import datetime

class MemoryItem(BaseModel):
    id: str = Field(description="Unique identifier for the memory.")
    category: str = Field(description="Category of the memory (e.g., 'project_information').")
    content: str = Field(description="The actual memory content to store.")
    timestamp: datetime = Field(description="Time when the memory was stored or last updated.")
