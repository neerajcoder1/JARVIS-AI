import pytest
from unittest.mock import patch, MagicMock
from app.tools.applications import OpenApplicationTool, CloseApplicationTool
from app.tools.system_info import GetSystemInfoTool
from app.tools.time_tool import GetCurrentTimeTool
import psutil

def test_open_application_allowlist():
    tool = OpenApplicationTool()
    
    # Supported
    with patch("subprocess.Popen") as mock_popen:
        result = tool.execute(application="chrome")
        assert result.success is True
        mock_popen.assert_called_with(["cmd", "/c", "start", "chrome"], shell=False)
        
    # Unsupported
    result = tool.execute(application="photoshop")
    assert result.success is False
    assert "not supported" in result.message

def test_close_application_allowlist():
    tool = CloseApplicationTool()
    
    # Unsupported
    result = tool.execute(application="photoshop")
    assert result.success is False
    assert "not supported" in result.message

    # Supported but not running
    with patch("psutil.process_iter", return_value=[]):
        result = tool.execute(application="chrome")
        assert result.success is False
        assert "not currently running" in result.message

    # Supported and running
    mock_proc = MagicMock()
    mock_proc.info = {'name': 'chrome.exe'}
    with patch("psutil.process_iter", return_value=[mock_proc]):
        result = tool.execute(application="chrome")
        assert result.success is True
        mock_proc.terminate.assert_called_once()

def test_system_info():
    tool = GetSystemInfoTool()
    result = tool.execute()
    assert result.success is True
    assert "Operating System" in result.message
    assert "CPU" in result.message
    assert "RAM" in result.message

def test_time_tool():
    tool = GetCurrentTimeTool()
    result = tool.execute()
    assert result.success is True
    assert "The current time is" in result.message
