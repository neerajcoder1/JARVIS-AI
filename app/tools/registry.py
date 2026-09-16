from typing import Dict, List, Type, Optional
from app.tools.base import BaseTool
from app.tools.errors import ToolError, ToolNotFoundError
from app.core.logger import logger

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """Register a tool instance."""
        if tool.name in self._tools:
            logger.warning(f"Tool with name '{tool.name}' is already registered. Skipping.")
            return
        self._tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")

    def unregister(self, tool_name: str) -> None:
        """Unregister a tool by name."""
        if tool_name in self._tools:
            del self._tools[tool_name]
            logger.info(f"Unregistered tool: {tool_name}")

    def get(self, tool_name: str) -> BaseTool:
        """Get a tool by name, raising ToolNotFoundError if missing."""
        if tool_name not in self._tools:
            raise ToolNotFoundError(f"Tool '{tool_name}' not found in registry.")
        return self._tools[tool_name]

    def list_tools(self) -> List[Dict[str, str]]:
        """List all available tools and their metadata."""
        return [
            {
                "name": t.name,
                "description": t.description,
                "permission": t.permission_level.value
            } for t in self._tools.values()
        ]

# Global registry instance
registry = ToolRegistry()
