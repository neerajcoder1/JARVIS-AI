import pytest
from app.tools.router import route_tools, TOOL_GROUPS

def set_equal(l1, l2):
    return set(l1) == set(l2)

def test_router_general_knowledge():
    tools = route_tools("What is Python?")
    assert tools == []

def test_router_system():
    tools = route_tools("What time is it?")
    assert set_equal(tools, TOOL_GROUPS["SYSTEM"])

def test_router_application():
    tools = route_tools("Open Calculator")
    # Because 'open' also triggers browser 'open website' overlap potentially?
    # Wait, 'open' triggers BROWSER and APPLICATION depending on the regex.
    # Let's check what it actually outputs.
    assert "open_application" in tools

def test_router_browser():
    tools = route_tools("Open Google")
    assert "browser_open" in tools

def test_router_filesystem_read():
    tools = route_tools("List files on my Desktop")
    assert "filesystem_list" in tools
    # "List" and "files" triggers READ. No write action word.
    assert "filesystem_delete" not in tools

def test_router_filesystem_write_create():
    tools = route_tools("Create test.txt on my Desktop")
    assert "filesystem_create_file" in tools

def test_router_filesystem_write_delete():
    tools = route_tools("Delete test.txt")
    assert "filesystem_delete" in tools

def test_router_ambiguous():
    tools = route_tools("Just checking things")
    assert tools == []

def test_router_unknown_category():
    tools = route_tools("Paint a picture")
    assert tools == []
