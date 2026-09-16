import pytest
from unittest.mock import patch, MagicMock
from app.tools.power import (
    ShutdownComputerTool, 
    RestartComputerTool, 
    SleepComputerTool, 
    LogoffComputerTool
)
from app.tools.permissions import PermissionLevel

def test_power_tools_registration_and_schemas():
    tools = [
        ShutdownComputerTool(),
        RestartComputerTool(),
        SleepComputerTool(),
        LogoffComputerTool()
    ]
    
    names = [t.name for t in tools]
    assert "shutdown_computer" in names
    assert "restart_computer" in names
    assert "sleep_computer" in names
    assert "logoff_computer" in names
    
    for tool in tools:
        assert tool.permission_level == PermissionLevel.CONFIRM
        assert tool.input_schema is not None
        assert hasattr(tool, "get_confirmation_message")

@patch("app.tools.power.subprocess.Popen")
def test_shutdown_execution(mock_popen):
    tool = ShutdownComputerTool()
    res = tool._execute()
    assert res.success is True
    # Verify shell is False and arbitrary commands are not executed
    mock_popen.assert_called_once_with(["shutdown", "/s", "/t", "0"], shell=False)

@patch("app.tools.power.subprocess.Popen")
def test_restart_execution(mock_popen):
    tool = RestartComputerTool()
    res = tool._execute()
    assert res.success is True
    mock_popen.assert_called_once_with(["shutdown", "/r", "/t", "0"], shell=False)

@patch("app.tools.power.subprocess.Popen")
def test_sleep_execution(mock_popen):
    tool = SleepComputerTool()
    res = tool._execute()
    assert res.success is True
    mock_popen.assert_called_once_with(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], shell=False)

@patch("app.tools.power.subprocess.Popen")
def test_logoff_execution(mock_popen):
    tool = LogoffComputerTool()
    res = tool._execute()
    assert res.success is True
    mock_popen.assert_called_once_with(["shutdown", "/l"], shell=False)
