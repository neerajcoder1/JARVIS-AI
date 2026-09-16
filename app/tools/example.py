from typing import Dict, Any
from pydantic import BaseModel
from app.tools.base import BaseTool
from app.tools.schemas import ToolResult
from app.tools.permissions import PermissionLevel

class ExampleArgs(BaseModel):
    action: str

class SafeExampleTool(BaseTool):
    @property
    def name(self) -> str:
        return "safe_example_tool"
        
    @property
    def description(self) -> str:
        return "A safe example tool that does nothing dangerous."
        
    @property
    def permission_level(self) -> PermissionLevel:
        return PermissionLevel.SAFE
        
    @property
    def input_schema(self) -> type[BaseModel]:
        return ExampleArgs

    def _execute(self, action: str) -> ToolResult:
        return ToolResult(success=True, message=f"Safely executed {action}")

class ConfirmExampleTool(BaseTool):
    @property
    def name(self) -> str:
        return "confirm_example_tool"
        
    @property
    def description(self) -> str:
        return "A tool that requires user confirmation."
        
    @property
    def permission_level(self) -> PermissionLevel:
        return PermissionLevel.CONFIRM
        
    @property
    def input_schema(self) -> type[BaseModel]:
        return ExampleArgs

    def _execute(self, action: str) -> ToolResult:
        return ToolResult(success=True, message=f"Confirmed and executed {action}")

class RestrictedExampleTool(BaseTool):
    @property
    def name(self) -> str:
        return "restricted_example_tool"
        
    @property
    def description(self) -> str:
        return "A tool that is restricted."
        
    @property
    def permission_level(self) -> PermissionLevel:
        return PermissionLevel.RESTRICTED
        
    @property
    def input_schema(self) -> type[BaseModel]:
        return ExampleArgs

    def _execute(self, action: str) -> ToolResult:
        return ToolResult(success=True, message=f"Restricted executed {action}")
