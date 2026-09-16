import pytest
from unittest.mock import patch, MagicMock
from app.tools.browser import OpenWebsiteTool, SearchWebTool, is_safe_url

def test_url_validation():
    # Valid
    assert is_safe_url("https://www.google.com") is True
    assert is_safe_url("http://example.com") is True
    assert is_safe_url("https://youtube.com/watch?v=123") is True
    assert is_safe_url("HTTP://google.com") is True
    
    # Invalid protocols
    assert is_safe_url("file:///C:/windows/system32/cmd.exe") is False
    assert is_safe_url("javascript:alert(1)") is False
    assert is_safe_url("data:text/html,<h1>Hello</h1>") is False
    assert is_safe_url("vbscript:msgbox('hi')") is False
    
    # Missing netloc
    assert is_safe_url("https://") is False
    assert is_safe_url("http:/") is False
    
    # Plain executables or shell commands
    assert is_safe_url("C:\\test.exe") is False
    assert is_safe_url("cmd.exe /c calc") is False
    assert is_safe_url("rm -rf /") is False

def test_open_website_tool():
    tool = OpenWebsiteTool()
    
    # Rejects unsafe
    res = tool.execute(url="file:///C:/test.exe")
    assert res.success is False
    assert "security reasons" in res.message
    
    res = tool.execute(url="javascript:alert(1)")
    assert res.success is False
    
    # Accepts safe
    with patch("webbrowser.open") as mock_open:
        mock_open.return_value = True
        res = tool.execute(url="https://google.com")
        assert res.success is True
        mock_open.assert_called_with("https://google.com")

def test_search_web_tool():
    tool = SearchWebTool()
    
    # Empty query
    res = tool.execute(query="   ")
    assert res.success is False
    
    # Normal query
    with patch("webbrowser.open") as mock_open:
        mock_open.return_value = True
        res = tool.execute(query="Python FastAPI tutorials")
        assert res.success is True
        
        # Verify it encoded properly and constructed the URL internally
        expected_url = "https://www.google.com/search?q=Python+FastAPI+tutorials"
        mock_open.assert_called_with(expected_url)
        
    # Malicious injection attempt in query
    with patch("webbrowser.open") as mock_open:
        mock_open.return_value = True
        res = tool.execute(query="javascript:alert(1)")
        assert res.success is True
        
        # Verify it safely encoded it as a search term rather than passing it as a URL
        expected_url = "https://www.google.com/search?q=javascript%3Aalert%281%29"
        mock_open.assert_called_with(expected_url)
