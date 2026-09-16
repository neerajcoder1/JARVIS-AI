import pytest
from unittest.mock import patch, MagicMock
from app.tools.screen import InspectScreenTool
from app.tools.permissions import PermissionLevel
from app.tools.router import route_tools

def test_screen_tool_metadata():
    tool = InspectScreenTool()
    assert tool.name == "inspect_screen"
    assert tool.permission_level == PermissionLevel.CONFIRM

def test_screen_tool_redaction():
    tool = InspectScreenTool()
    
    raw_text = "Here is my api_key: sk-12345678901234567890123456789012. Also my password: secretpassword"
    redacted = tool._redact_sensitive_info(raw_text)
    
    assert "sk-" not in redacted
    assert "[REDACTED API KEY]" in redacted
    assert "secretpassword" not in redacted
    assert "[REDACTED]" in redacted

@patch("app.tools.screen.ImageGrab.grab")
@patch("app.tools.screen.pytesseract.image_to_string")
def test_screen_tool_execution(mock_ocr, mock_grab):
    tool = InspectScreenTool()
    
    mock_img = MagicMock()
    mock_grab.return_value = mock_img
    mock_ocr.return_value = "Normal safe screen text with no secrets."
    
    result = tool.execute()
    
    assert result.success is True
    assert "safe screen text" in result.message
    # verify the image was closed to free memory
    mock_img.close.assert_called_once()

def test_screen_routing():
    assert "inspect_screen" in route_tools("What is on my screen?")
    assert "inspect_screen" in route_tools("Read this error")
    assert "inspect_screen" in route_tools("What does this webpage say?")
