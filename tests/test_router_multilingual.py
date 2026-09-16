import pytest
from app.tools.router import route_tools

def test_router_multilingual_english():
    assert "filesystem_list" in route_tools("List files on desktop")
    assert "browser_open" in route_tools("Open google")
    assert not route_tools("What is python?")

def test_router_multilingual_hindi():
    assert "filesystem_list" in route_tools("Mere Desktop par kaun kaun si files hain")
    assert "filesystem_list" in route_tools("Desktop par files dikhao")
    assert "browser_open" in route_tools("Google dhundo aur open karo")
    assert "browser_open" in route_tools("FastAPI search karo")

def test_router_multilingual_hinglish_mixed():
    tools = route_tools("Notepad kholo")
    assert "open_application" in tools
    
    tools2 = route_tools("Ek file banao")
    assert "filesystem_create_file" in tools2

def test_router_multilingual_simple():
    # Should not match tools for basic facts
    assert not route_tools("Python kya hai?")
    assert not route_tools("Tumhara naam kya hai?")
