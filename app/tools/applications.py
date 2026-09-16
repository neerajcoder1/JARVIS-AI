import subprocess
import psutil
from typing import ClassVar, Dict, Any, List, Union
from pydantic import BaseModel, Field
from app.tools.base import BaseTool
from app.tools.schemas import ToolResult
from app.tools.permissions import PermissionLevel
from app.core.logger import logger

class AppArgs(BaseModel):
    application: str = Field(description="The name of the application to interact with (e.g. 'chrome', 'notepad').")

# Strict allowlist: Key is the lowercase normalized name.
# Value contains the command to open it, and the exact process name to close it.
ALLOWLIST: Dict[str, Dict[str, Union[str, List[str]]]] = {
    "chrome": {
        "open": ["cmd", "/c", "start", "chrome"],
        "process_name": "chrome.exe"
    },
    "visual studio code": {
        "open": ["cmd", "/c", "code"],
        "process_name": "Code.exe"
    },
    "vscode": {
        "open": ["cmd", "/c", "code"],
        "process_name": "Code.exe"
    },
    "notepad": {
        "open": ["notepad.exe"],
        "process_name": "notepad.exe"
    },
    "calculator": {
        "open": ["calc.exe"],
        "process_name": "CalculatorApp.exe"
    },
    "file explorer": {
        "open": ["explorer.exe"],
        "process_name": "explorer.exe"
    }
}

class OpenApplicationTool(BaseTool):
    @property
    def name(self) -> str:
        return "open_application"
        
    @property
    def description(self) -> str:
        return "Opens a known, supported Windows application from a safe allowlist."
        
    @property
    def permission_level(self) -> PermissionLevel:
        return PermissionLevel.SAFE
        
    @property
    def input_schema(self) -> type[BaseModel]:
        return AppArgs

    def _execute(self, application: str) -> ToolResult:
        app_key = application.lower().strip()
        if app_key not in ALLOWLIST:
            return ToolResult(
                success=False,
                message=f"That application is not supported. Supported applications are: {', '.join(set(ALLOWLIST.keys()))}"
            )
            
        cmd = ALLOWLIST[app_key]["open"]
        try:
            # We explicitly pass the predefined command list from our allowlist, NOT from the LLM.
            # This completely prevents arbitrary shell execution.
            subprocess.Popen(cmd, shell=False)
            return ToolResult(success=True, message=f"{application.title()} opened successfully.")
        except Exception as e:
            logger.error(f"Failed to open {application}: {e}")
            return ToolResult(success=False, message=f"{application.title()} could not be opened.")


class CloseApplicationTool(BaseTool):
    @property
    def name(self) -> str:
        return "close_application"
        
    @property
    def description(self) -> str:
        return "Closes a known, supported Windows application. This will forcefully terminate the application."
        
    @property
    def permission_level(self) -> PermissionLevel:
        return PermissionLevel.CONFIRM
        
    @property
    def input_schema(self) -> type[BaseModel]:
        return AppArgs

    def _execute(self, application: str) -> ToolResult:
        app_key = application.lower().strip()
        if app_key not in ALLOWLIST:
            return ToolResult(
                success=False,
                message=f"That application is not supported. Supported applications are: {', '.join(set(ALLOWLIST.keys()))}"
            )
            
        process_name = ALLOWLIST[app_key]["process_name"]
        terminated_count = 0
        
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and proc.info['name'].lower() == process_name.lower():
                    proc.terminate()
                    terminated_count += 1
                    
            if terminated_count > 0:
                return ToolResult(success=True, message=f"{application.title()} was closed successfully.")
            else:
                return ToolResult(success=False, message=f"{application.title()} is not currently running.")
        except psutil.AccessDenied:
            logger.error(f"Access denied closing {application}")
            return ToolResult(success=False, message=f"I don't have permission to close {application.title()}.")
        except Exception as e:
            logger.error(f"Error closing {application}: {e}")
            return ToolResult(success=False, message=f"An error occurred while trying to close {application.title()}.")
