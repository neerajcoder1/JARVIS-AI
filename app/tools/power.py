import subprocess
from pydantic import BaseModel
from app.tools.base import BaseTool
from app.tools.schemas import ToolResult
from app.tools.permissions import PermissionLevel
from app.core.logger import logger

class EmptyArgs(BaseModel):
    pass

class ShutdownComputerTool(BaseTool):
    @property
    def name(self) -> str:
        return "shutdown_computer"
        
    @property
    def description(self) -> str:
        return "Shut down the Windows computer. This operation requires explicit user confirmation."
        
    @property
    def permission_level(self) -> PermissionLevel:
        return PermissionLevel.CONFIRM
        
    @property
    def input_schema(self) -> type[BaseModel]:
        return EmptyArgs
        
    def get_confirmation_message(self, **kwargs) -> str:
        return "Sir, shutting down your laptop will close your current session. Should I proceed?"

    def _execute(self) -> ToolResult:
        try:
            # shell=False and fixed arguments
            subprocess.Popen(["shutdown", "/s", "/t", "0"], shell=False)
            return ToolResult(success=True, message="Shutting down the computer.")
        except Exception as e:
            logger.error(f"Failed to shutdown: {e}")
            return ToolResult(success=False, message="Failed to execute shutdown command.")

class RestartComputerTool(BaseTool):
    @property
    def name(self) -> str:
        return "restart_computer"
        
    @property
    def description(self) -> str:
        return "Restart the Windows computer. This operation requires explicit user confirmation."
        
    @property
    def permission_level(self) -> PermissionLevel:
        return PermissionLevel.CONFIRM
        
    @property
    def input_schema(self) -> type[BaseModel]:
        return EmptyArgs
        
    def get_confirmation_message(self, **kwargs) -> str:
        return "Sir, restarting your laptop will close the current session. Should I proceed?"

    def _execute(self) -> ToolResult:
        try:
            subprocess.Popen(["shutdown", "/r", "/t", "0"], shell=False)
            return ToolResult(success=True, message="Restarting the computer.")
        except Exception as e:
            logger.error(f"Failed to restart: {e}")
            return ToolResult(success=False, message="Failed to execute restart command.")

class SleepComputerTool(BaseTool):
    @property
    def name(self) -> str:
        return "sleep_computer"
        
    @property
    def description(self) -> str:
        return "Put the Windows computer into sleep mode. This operation requires explicit user confirmation."
        
    @property
    def permission_level(self) -> PermissionLevel:
        return PermissionLevel.CONFIRM
        
    @property
    def input_schema(self) -> type[BaseModel]:
        return EmptyArgs
        
    def get_confirmation_message(self, **kwargs) -> str:
        return "Sir, should I put the laptop to sleep?"

    def _execute(self) -> ToolResult:
        try:
            # standard way to sleep windows
            subprocess.Popen(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], shell=False)
            return ToolResult(success=True, message="Putting the computer to sleep.")
        except Exception as e:
            logger.error(f"Failed to sleep: {e}")
            return ToolResult(success=False, message="Failed to execute sleep command.")

class LogoffComputerTool(BaseTool):
    @property
    def name(self) -> str:
        return "logoff_computer"
        
    @property
    def description(self) -> str:
        return "Log off the current Windows user session. This operation requires explicit user confirmation."
        
    @property
    def permission_level(self) -> PermissionLevel:
        return PermissionLevel.CONFIRM
        
    @property
    def input_schema(self) -> type[BaseModel]:
        return EmptyArgs
        
    def get_confirmation_message(self, **kwargs) -> str:
        return "Sir, should I log off Windows?"

    def _execute(self) -> ToolResult:
        try:
            subprocess.Popen(["shutdown", "/l"], shell=False)
            return ToolResult(success=True, message="Logging off.")
        except Exception as e:
            logger.error(f"Failed to logoff: {e}")
            return ToolResult(success=False, message="Failed to execute logoff command.")
