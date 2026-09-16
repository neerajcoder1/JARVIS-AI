from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class ToolResult(BaseModel):
    """Standardized output structure for all tools."""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
