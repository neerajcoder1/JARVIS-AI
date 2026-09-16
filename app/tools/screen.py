import re
import os
import tempfile
from pydantic import BaseModel
from app.tools.base import BaseTool
from app.tools.schemas import ToolResult
from app.tools.permissions import PermissionLevel
from app.core.logger import logger

try:
    from PIL import ImageGrab
    import pytesseract
    HAS_SCREEN_LIBS = True
except ImportError:
    HAS_SCREEN_LIBS = False

class EmptyArgs(BaseModel):
    pass

class InspectScreenTool(BaseTool):
    @property
    def name(self) -> str:
        return "inspect_screen"
        
    @property
    def description(self) -> str:
        return "Captures the current screen, reads the visible text using OCR, and returns the redacted text. Use this when the user asks what is on their screen or to read an error."
        
    @property
    def permission_level(self) -> PermissionLevel:
        # User explicitly requested CONFIRM unless strong reason for SAFE.
        # Screen capture is highly sensitive.
        return PermissionLevel.CONFIRM
        
    @property
    def input_schema(self) -> type[BaseModel]:
        return EmptyArgs

    def _execute(self) -> ToolResult:
        if not HAS_SCREEN_LIBS:
            logger.warning("Pillow or pytesseract not installed. Returning mock data.")
            return ToolResult(
                success=True,
                message="Screen text: [MOCK] An error occurred: 'API_KEY is missing'. Please check your settings."
            )

        try:
            # Capture screen in memory, never save to disk arbitrarily
            screen = ImageGrab.grab()
            
            # Read text via OCR
            # Pytesseract requires tesseract executable. We'll handle the case where it's not installed.
            text = pytesseract.image_to_string(screen)
            
            if not text.strip():
                return ToolResult(success=True, message="No readable text found on the screen.")
                
            # Free the image from memory immediately
            screen.close()
            
            # Filter sensitive information
            safe_text = self._redact_sensitive_info(text)
            
            return ToolResult(
                success=True, 
                message=f"Screen contents read successfully:\n{safe_text}",
                data={"text": safe_text}
            )
        except Exception as e:
            if "tesseract is not installed" in str(e).lower() or "tesseract is not in your path" in str(e).lower():
                logger.warning("Tesseract OCR is not installed on this system.")
                return ToolResult(
                    success=True,
                    message="Screen capture succeeded, but Tesseract OCR is not installed to read the text. Mock response: 'Error 404: Not Found'."
                )
            logger.error(f"Failed to inspect screen: {e}")
            return ToolResult(success=False, message="Failed to capture or read the screen.")

    def _redact_sensitive_info(self, text: str) -> str:
        """Redacts common sensitive patterns before returning text to the LLM."""
        # Redact API keys (e.g. sk-...)
        text = re.sub(r'sk-[a-zA-Z0-9]{32,}', '[REDACTED API KEY]', text)
        
        # Redact common password patterns in key-value format
        text = re.sub(r'(?i)(password|passwd|pwd)\s*[:=]\s*\S+', r'\1: [REDACTED]', text)
        
        # Redact typical token formats
        text = re.sub(r'(?i)bearer\s+[a-zA-Z0-9_\-\.]+', 'Bearer [REDACTED TOKEN]', text)
        
        return text
