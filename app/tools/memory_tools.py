from pydantic import BaseModel, Field
from typing import Optional
from app.tools.base import BaseTool
from app.tools.schemas import ToolResult
from app.tools.permissions import PermissionLevel
from app.memory.manager import MemoryManager
from app.memory.retrieval import MemoryRetrieval

class SaveMemoryArgs(BaseModel):
    category: str = Field(description="Category (user_preferences, project_information, recurring_preferences, useful_facts)")
    content: str = Field(description="Information to remember")

class RetrieveMemoryArgs(BaseModel):
    query: Optional[str] = Field(default=None, description="Search query")
    category: Optional[str] = Field(default=None, description="Category filter")

class DeleteMemoryArgs(BaseModel):
    memory_id: str = Field(description="ID of memory to delete")

class UpdateMemoryArgs(BaseModel):
    memory_id: str = Field(description="ID of memory to update")
    category: str = Field(description="New category")
    content: str = Field(description="New content")

class SaveMemoryTool(BaseTool):
    @property
    def name(self) -> str: return "save_memory"
    @property
    def description(self) -> str: return "Save facts or project info to persistent memory. Do NOT save secrets."
    @property
    def permission_level(self) -> PermissionLevel: return PermissionLevel.SAFE
    @property
    def input_schema(self) -> type[BaseModel]: return SaveMemoryArgs

    def _execute(self, category: str, content: str) -> ToolResult:
        try:
            manager = MemoryManager()
            memory_id = manager.save_memory(category, content)
            return ToolResult(success=True, message=f"Saved memory ID: {memory_id}")
        except Exception as e:
            return ToolResult(success=False, message=str(e))

class RetrieveMemoryTool(BaseTool):
    @property
    def name(self) -> str: return "retrieve_memory"
    @property
    def description(self) -> str: return "Retrieve stored information from persistent memory."
    @property
    def permission_level(self) -> PermissionLevel: return PermissionLevel.SAFE
    @property
    def input_schema(self) -> type[BaseModel]: return RetrieveMemoryArgs

    def _execute(self, query: str = None, category: str = None) -> ToolResult:
        try:
            retrieval = MemoryRetrieval()
            results = retrieval.search(query=query, category=category)
            if not results:
                return ToolResult(success=True, message="No matching memories found.")
            out = "\n".join([f"[{r.category}] (ID: {r.id}): {r.content}" for r in results])
            return ToolResult(success=True, message=out, data=[r.model_dump(mode='json') for r in results])
        except Exception as e:
            return ToolResult(success=False, message=str(e))

class DeleteMemoryTool(BaseTool):
    @property
    def name(self) -> str: return "delete_memory"
    @property
    def description(self) -> str: return "Delete a memory entry by ID."
    @property
    def permission_level(self) -> PermissionLevel: return PermissionLevel.SAFE
    @property
    def input_schema(self) -> type[BaseModel]: return DeleteMemoryArgs

    def _execute(self, memory_id: str) -> ToolResult:
        try:
            manager = MemoryManager()
            if manager.delete_memory(memory_id):
                return ToolResult(success=True, message=f"Deleted memory {memory_id}.")
            return ToolResult(success=False, message=f"Memory {memory_id} not found.")
        except Exception as e:
            return ToolResult(success=False, message=str(e))

class UpdateMemoryTool(BaseTool):
    @property
    def name(self) -> str: return "update_memory"
    @property
    def description(self) -> str: return "Update an existing memory by ID."
    @property
    def permission_level(self) -> PermissionLevel: return PermissionLevel.SAFE
    @property
    def input_schema(self) -> type[BaseModel]: return UpdateMemoryArgs

    def _execute(self, memory_id: str, category: str, content: str) -> ToolResult:
        try:
            manager = MemoryManager()
            if manager.update_memory(memory_id, category, content):
                return ToolResult(success=True, message=f"Updated memory {memory_id}.")
            return ToolResult(success=False, message=f"Memory {memory_id} not found.")
        except Exception as e:
            return ToolResult(success=False, message=str(e))
