from datetime import datetime
from pydantic import BaseModel
from app.tools.base import BaseTool
from app.tools.schemas import ToolResult
from app.tools.permissions import PermissionLevel

class EmptyArgs(BaseModel):
    pass

class GetCurrentTimeTool(BaseTool):
    @property
    def name(self) -> str:
        return "get_current_time"
        
    @property
    def description(self) -> str:
        return "Gets the current local system time and date."
        
    @property
    def permission_level(self) -> PermissionLevel:
        return PermissionLevel.SAFE
        
    @property
    def input_schema(self) -> type[BaseModel]:
        return EmptyArgs

    def _execute(self) -> ToolResult:
        try:
            now = datetime.now()
            time_str = now.strftime("%I:%M %p")
            date_str = now.strftime("%A, %B %d, %Y")
            
            return ToolResult(
                success=True, 
                message=f"The current time is {time_str} on {date_str}.",
                data={"time": time_str, "date": date_str}
            )
        except Exception as e:
            return ToolResult(success=False, message="Failed to get current time.")
