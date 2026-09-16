import json
from typing import List, Dict, Any, Tuple
from app.tools.registry import registry
from app.tools.permissions import PermissionManager, PermissionLevel
from app.tools.schemas import ToolResult
from app.tools.errors import ToolError, ToolNotFoundError, ToolPermissionError
from app.core.logger import logger

class ToolExecutor:
    """Handles parsing, permission checks, and execution of tool calls."""
    
    @staticmethod
    def get_openai_tools(allowed_names: List[str] = None) -> List[Dict[str, Any]]:
        """Converts registered tools into OpenAI's expected tool schema."""
        tools = []
        for meta in registry.list_tools():
            if allowed_names is not None and meta["name"] not in allowed_names:
                continue
            tool = registry.get(meta["name"])
            
            # Simple conversion of Pydantic schema to JSON schema
            schema = tool.input_schema.model_json_schema()
            
            tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": schema
                }
            })
        return tools

    @staticmethod
    def handle_tool_call(tool_name: str, arguments: Dict[str, Any], user_confirmed: bool = False) -> Tuple[bool, str, Any]:
        """
        Validates and executes a tool call.
        Returns (success, message, result_data)
        If CONFIRM is needed and user_confirmed is False, returns (False, confirmation_message, None)
        """
        try:
            # 1. Validate tool exists
            tool = registry.get(tool_name)
            
            # 2. Permission layer check
            # This will raise ToolPermissionError if not allowed or needs confirmation
            PermissionManager.check_permission(tool.name, tool.permission_level, user_confirmation=user_confirmed)
            
            # 3. Execute
            logger.info(f"Executing tool {tool.name}")
            result = tool.execute(**arguments)
            
            if result.success:
                return True, result.message, result.data
            else:
                return False, result.message, None
                
        except ToolPermissionError as e:
            # Handle CONFIRM and RESTRICTED levels requiring user confirmation
            tool = registry.get(tool_name)
            if tool.permission_level in (PermissionLevel.CONFIRM, PermissionLevel.RESTRICTED) and not user_confirmed:
                if hasattr(tool, "get_confirmation_message"):
                    msg = tool.get_confirmation_message(**arguments)
                else:
                    msg = f"This action will {tool.description.lower()}. Do you want me to continue?"
                return False, msg, "NEEDS_CONFIRMATION"
            
            # Otherwise it's restricted or denied
            logger.warning(f"Permission denied for {tool_name}: {e}")
            return False, f"I am not allowed to execute {tool_name}.", None
            
        except ToolNotFoundError as e:
            logger.error(str(e))
            return False, f"I don't have a tool named {tool_name}.", None
            
        except Exception as e:
            logger.error(f"Unexpected error handling tool {tool_name}: {e}")
            return False, f"An error occurred while running {tool_name}.", None
