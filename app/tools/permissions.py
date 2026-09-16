from enum import Enum
from app.tools.errors import ToolPermissionError

class PermissionLevel(str, Enum):
    SAFE = "SAFE"
    CONFIRM = "CONFIRM"
    RESTRICTED = "RESTRICTED"

class PermissionManager:
    @staticmethod
    def check_permission(tool_name: str, level: PermissionLevel, user_confirmation: bool = False) -> bool:
        """
        Evaluate if a tool is allowed to execute.
        SAFE -> Always True
        CONFIRM -> True if user_confirmation is True, else False
        RESTRICTED -> Always False (for phase 2 foundation)
        """
        if level in (PermissionLevel.RESTRICTED, PermissionLevel.CONFIRM):
            if not user_confirmation:
                raise ToolPermissionError(f"Execution of '{tool_name}' requires explicit user confirmation.")
            return True
            
        if level == PermissionLevel.SAFE:
            return True
            
        raise ToolPermissionError(f"Unknown permission level: {level}")
