import pytest
from unittest.mock import patch, MagicMock
from app.tools.input import MouseMoveTool, MouseClickTool, KeyboardTypeTool, KeyboardPressTool
from app.tools.permissions import PermissionLevel
from app.tools.router import route_tools

def test_input_tools_metadata():
    mm = MouseMoveTool()
    mc = MouseClickTool()
    kt = KeyboardTypeTool()
    kp = KeyboardPressTool()
    
    assert mm.name == "mouse_move"
    assert mc.name == "mouse_click"
    assert kt.name == "keyboard_type"
    assert kp.name == "keyboard_press"
    
    assert mm.permission_level == PermissionLevel.CONFIRM
    assert mc.permission_level == PermissionLevel.CONFIRM
    assert kt.permission_level == PermissionLevel.CONFIRM
    assert kp.permission_level == PermissionLevel.CONFIRM

@patch("app.tools.input.pyautogui.moveTo")
def test_mouse_move_execution(mock_move):
    tool = MouseMoveTool()
    res = tool.execute(x=100, y=200)
    assert res.success
    mock_move.assert_called_once_with(100, 200, duration=0.5)

@patch("app.tools.input.pyautogui.click")
def test_mouse_click_execution(mock_click):
    tool = MouseClickTool()
    res = tool.execute(button="left", clicks=2, x=50, y=50)
    assert res.success
    mock_click.assert_called_once_with(x=50, y=50, clicks=2, button="left")

@patch("app.tools.input.pyautogui.typewrite")
def test_keyboard_type_execution(mock_type):
    tool = KeyboardTypeTool()
    res = tool.execute(text="Hello", interval=0.1)
    assert res.success
    mock_type.assert_called_once_with("Hello", interval=0.1)

@patch("app.tools.input.pyautogui.hotkey")
def test_keyboard_press_hotkey(mock_hotkey):
    tool = KeyboardPressTool()
    res = tool.execute(keys=["ctrl", "c"])
    assert res.success
    mock_hotkey.assert_called_once_with("ctrl", "c")

@patch("app.tools.input.pyautogui.press")
def test_keyboard_press_single(mock_press):
    tool = KeyboardPressTool()
    res = tool.execute(keys=["enter"])
    assert res.success
    mock_press.assert_called_once_with("enter")

def test_input_routing():
    assert "mouse_click" in route_tools("Click the search box")
    assert "keyboard_type" in route_tools("Type Python tutorial")
    assert "keyboard_press" in route_tools("Press Enter")
