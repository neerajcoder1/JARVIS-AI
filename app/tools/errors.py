class ToolError(Exception):
    """Base exception for tool-related errors."""
    pass

class ToolNotFoundError(ToolError):
    """Raised when a requested tool is not found in the registry."""
    pass

class ToolPermissionError(ToolError):
    """Raised when a tool execution is denied due to permission constraints."""
    pass

class ToolExecutionError(ToolError):
    """Raised when a tool fails during execution."""
    pass
