from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel
from app.tools.schemas import ToolResult
from app.tools.permissions import PermissionLevel
from app.core.logger import logger

class BaseTool(ABC):
    """Abstract base class for all JARVIS tools."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """The unique name of the tool."""
        pass
        
    @property
    @abstractmethod
    def description(self) -> str:
        """A detailed description of what the tool does."""
        pass
        
    @property
    @abstractmethod
    def permission_level(self) -> PermissionLevel:
        """The permission level required to execute the tool."""
        pass
        
    @property
    @abstractmethod
    def input_schema(self) -> type[BaseModel]:
        """Pydantic model representing the expected arguments."""
        pass

    @abstractmethod
    def _execute(self, **kwargs) -> ToolResult:
        """Internal execution logic implemented by specific tools."""
        pass

    def execute(self, **kwargs) -> ToolResult:
        """
        Public execution method. Validates arguments against the schema,
        then calls the internal _execute method, capturing exceptions.
        """
        try:
            logger.info(f"Executing tool '{self.name}' with args: {kwargs}")
            
            # Validate kwargs using the defined schema
            validated_args = self.input_schema(**kwargs).model_dump()
            
            # Execute the tool
            result = self._execute(**validated_args)
            
            return result
        except Exception as e:
            logger.error(f"Tool execution failed for '{self.name}': {e}")
            return ToolResult(
                success=False,
                message=f"Error executing {self.name}: {str(e)}",
                error=str(e)
            )
