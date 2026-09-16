import time
from typing import Optional, List
from pydantic import BaseModel, Field
from app.tools.base import BaseTool
from app.tools.schemas import ToolResult
from app.tools.permissions import PermissionLevel
from app.core.logger import logger

try:
    import pyautogui
    pyautogui.FAILSAFE = True  # Move mouse to corner to abort
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False

class MouseMoveArgs(BaseModel):
    x: int = Field(description="The absolute X coordinate to move the mouse cursor to.")
    y: int = Field(description="The absolute Y coordinate to move the mouse cursor to.")
    duration: float = Field(default=0.5, description="The duration in seconds to animate the mouse movement. Default is 0.5s.")

class MouseClickArgs(BaseModel):
    button: str = Field(default="left", description="Which mouse button to click: 'left', 'right', or 'middle'.")
    clicks: int = Field(default=1, description="Number of times to click.")
    x: Optional[int] = Field(default=None, description="Optional X coordinate to click. If omitted, clicks current position.")
    y: Optional[int] = Field(default=None, description="Optional Y coordinate to click. If omitted, clicks current position.")

class KeyboardTypeArgs(BaseModel):
    text: str = Field(description="The text string to type out.")
    interval: float = Field(default=0.05, description="The delay in seconds between each keystroke. Default is 0.05s.")

class KeyboardPressArgs(BaseModel):
    keys: List[str] = Field(description="A list of key names to press together (e.g., ['ctrl', 'c'] or ['enter']).")

class MouseMoveTool(BaseTool):
    @property
    def name(self) -> str: return "mouse_move"
    @property
    def description(self) -> str: return "Moves the mouse cursor to a specific absolute X, Y screen coordinate."
    @property
    def permission_level(self) -> PermissionLevel: return PermissionLevel.CONFIRM
    @property
    def input_schema(self) -> type[BaseModel]: return MouseMoveArgs

    def _execute(self, x: int, y: int, duration: float = 0.5) -> ToolResult:
        if not HAS_PYAUTOGUI:
            return ToolResult(success=True, message=f"[MOCK] Moved mouse to ({x}, {y})")
        try:
            pyautogui.moveTo(x, y, duration=duration)
            return ToolResult(success=True, message=f"Successfully moved mouse to ({x}, {y})")
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to move mouse: {str(e)}")

class MouseClickTool(BaseTool):
    @property
    def name(self) -> str: return "mouse_click"
    @property
    def description(self) -> str: return "Clicks the mouse (left, right, or middle). Can optionally move to X, Y before clicking."
    @property
    def permission_level(self) -> PermissionLevel: return PermissionLevel.CONFIRM
    @property
    def input_schema(self) -> type[BaseModel]: return MouseClickArgs

    def _execute(self, button: str = "left", clicks: int = 1, x: int = None, y: int = None) -> ToolResult:
        if not HAS_PYAUTOGUI:
            return ToolResult(success=True, message=f"[MOCK] Clicked {button} {clicks} times at ({x}, {y})")
        try:
            if x is not None and y is not None:
                pyautogui.click(x=x, y=y, clicks=clicks, button=button)
                msg = f"Successfully clicked {button} {clicks} times at ({x}, {y})"
            else:
                pyautogui.click(clicks=clicks, button=button)
                msg = f"Successfully clicked {button} {clicks} times at current position"
            return ToolResult(success=True, message=msg)
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to click mouse: {str(e)}")

class KeyboardTypeTool(BaseTool):
    @property
    def name(self) -> str: return "keyboard_type"
    @property
    def description(self) -> str: return "Types out a string of text simulating individual keystrokes. Use for entering text into forms or documents."
    @property
    def permission_level(self) -> PermissionLevel: return PermissionLevel.CONFIRM
    @property
    def input_schema(self) -> type[BaseModel]: return KeyboardTypeArgs

    def _execute(self, text: str, interval: float = 0.05) -> ToolResult:
        if not HAS_PYAUTOGUI:
            return ToolResult(success=True, message=f"[MOCK] Typed: '{text}'")
        try:
            pyautogui.typewrite(text, interval=interval)
            return ToolResult(success=True, message=f"Successfully typed '{text}'")
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to type text: {str(e)}")

class KeyboardPressTool(BaseTool):
    @property
    def name(self) -> str: return "keyboard_press"
    @property
    def description(self) -> str: return "Presses one or more keyboard keys (e.g., ['enter'], ['ctrl', 'c'], ['tab']). Executes shortcuts or control actions."
    @property
    def permission_level(self) -> PermissionLevel: return PermissionLevel.CONFIRM
    @property
    def input_schema(self) -> type[BaseModel]: return KeyboardPressArgs

    def _execute(self, keys: List[str]) -> ToolResult:
        if not HAS_PYAUTOGUI:
            return ToolResult(success=True, message=f"[MOCK] Pressed keys: {keys}")
        try:
            if len(keys) == 1:
                pyautogui.press(keys[0])
            else:
                pyautogui.hotkey(*keys)
            return ToolResult(success=True, message=f"Successfully pressed {keys}")
        except Exception as e:
            return ToolResult(success=False, message=f"Failed to press keys: {str(e)}")
