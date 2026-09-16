import pytest
from app.tools.registry import ToolRegistry
from app.tools.permissions import PermissionManager, PermissionLevel
from app.tools.errors import ToolNotFoundError, ToolPermissionError, ToolError
from app.tools.example import SafeExampleTool, ConfirmExampleTool, RestrictedExampleTool
from app.tools.executor import ToolExecutor

def test_tool_registry():
    registry = ToolRegistry()
    safe_tool = SafeExampleTool()
    
    registry.register(safe_tool)
    assert len(registry.list_tools()) == 1
    
    # Should not raise exception anymore, just skips
    registry.register(safe_tool)
    assert len(registry.list_tools()) == 1
        
    tool = registry.get("safe_example_tool")
    assert tool.name == "safe_example_tool"
    
    with pytest.raises(ToolNotFoundError):
        registry.get("unknown_tool")
        
    registry.unregister("safe_example_tool")
    assert len(registry.list_tools()) == 0

def test_permissions():
    assert PermissionManager.check_permission("test", PermissionLevel.SAFE) is True
    
    assert PermissionManager.check_permission("test", PermissionLevel.CONFIRM, user_confirmation=True) is True
    
    with pytest.raises(ToolPermissionError):
        PermissionManager.check_permission("test", PermissionLevel.CONFIRM, user_confirmation=False)
        
    with pytest.raises(ToolPermissionError):
        PermissionManager.check_permission("test", PermissionLevel.RESTRICTED)

def test_tool_execution():
    safe_tool = SafeExampleTool()
    result = safe_tool.execute(action="test")
    assert result.success is True
    assert result.message == "Safely executed test"
    
    # Missing required argument
    result2 = safe_tool.execute()
    assert result2.success is False
    assert "error" in result2.message.lower()

def test_tool_executor():
    # We use the global registry for ToolExecutor
    from app.tools.registry import registry
    registry.register(SafeExampleTool())
    registry.register(ConfirmExampleTool())
    registry.register(RestrictedExampleTool())
    
    # SAFE
    success, msg, data = ToolExecutor.handle_tool_call("safe_example_tool", {"action": "run"})
    assert success is True
    
    # CONFIRM - Not confirmed
    success, msg, data = ToolExecutor.handle_tool_call("confirm_example_tool", {"action": "run"}, user_confirmed=False)
    assert success is False
    assert data == "NEEDS_CONFIRMATION"
    
    # CONFIRM - Confirmed
    success, msg, data = ToolExecutor.handle_tool_call("confirm_example_tool", {"action": "run"}, user_confirmed=True)
    assert success is True
    
    # RESTRICTED
    success, msg, data = ToolExecutor.handle_tool_call("restricted_example_tool", {"action": "run"}, user_confirmed=False)
    assert success is False
    assert data == "NEEDS_CONFIRMATION"
    
    # Unknown
    success, msg, data = ToolExecutor.handle_tool_call("unknown", {"action": "run"})
    assert success is False
    assert "don't have a tool" in msg
    
    # Clean up
    registry.unregister("safe_example_tool")
    registry.unregister("confirm_example_tool")
    registry.unregister("restricted_example_tool")
