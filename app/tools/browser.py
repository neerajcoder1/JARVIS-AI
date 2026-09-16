import webbrowser
from urllib.parse import urlparse, quote_plus
from pydantic import BaseModel, Field
from app.tools.base import BaseTool
from app.tools.schemas import ToolResult
from app.tools.permissions import PermissionLevel
from app.core.logger import logger

def is_safe_url(url: str) -> bool:
    """Strictly validates that a URL uses a safe protocol (http/https)."""
    try:
        parsed = urlparse(url)
        # Scheme must be exactly http or https (case-insensitive)
        if parsed.scheme.lower() not in ("http", "https"):
            return False
        # Must have a valid network location
        if not parsed.netloc:
            return False
        return True
    except Exception:
        return False

class OpenWebsiteArgs(BaseModel):
    url: str = Field(description="The full URL to open (e.g., 'https://www.google.com'). Must start with http:// or https://")

class SearchWebArgs(BaseModel):
    query: str = Field(description="The search query to look up on the web.")

class OpenWebsiteTool(BaseTool):
    @property
    def name(self) -> str:
        return "open_website"
        
    @property
    def description(self) -> str:
        return "Opens a specific, safe HTTP/HTTPS URL in the default web browser."
        
    @property
    def permission_level(self) -> PermissionLevel:
        return PermissionLevel.SAFE
        
    @property
    def input_schema(self) -> type[BaseModel]:
        return OpenWebsiteArgs

    def _execute(self, url: str) -> ToolResult:
        url = url.strip()
        
        # Security validation
        if not is_safe_url(url):
            logger.warning(f"Rejected unsafe URL attempt: {url}")
            return ToolResult(
                success=False,
                message="I cannot open that URL for security reasons. Only standard http/https websites are allowed."
            )
            
        try:
            # webbrowser.open passes the URL to the OS default protocol handler
            # Because we validated the scheme is http/https, this is safe
            opened = webbrowser.open(url)
            if opened:
                return ToolResult(success=True, message=f"Opened {url} successfully.")
            else:
                return ToolResult(success=False, message="I couldn't open the browser.")
        except Exception as e:
            logger.error(f"Error opening URL {url}: {e}")
            return ToolResult(success=False, message="An error occurred while trying to open the website.")


class SearchWebTool(BaseTool):
    @property
    def name(self) -> str:
        return "search_web"
        
    @property
    def description(self) -> str:
        return "Searches the web for a specific query using the default web browser."
        
    @property
    def permission_level(self) -> PermissionLevel:
        return PermissionLevel.SAFE
        
    @property
    def input_schema(self) -> type[BaseModel]:
        return SearchWebArgs

    def _execute(self, query: str) -> ToolResult:
        query = query.strip()
        if not query:
            return ToolResult(success=False, message="The search query cannot be empty.")
            
        # Construct a safe search URL internally using properly encoded query
        encoded_query = quote_plus(query)
        search_url = f"https://www.google.com/search?q={encoded_query}"
        
        try:
            opened = webbrowser.open(search_url)
            if opened:
                return ToolResult(success=True, message=f"Searched the web for '{query}'.")
            else:
                return ToolResult(success=False, message="I couldn't open the browser to search.")
        except Exception as e:
            logger.error(f"Error executing web search for '{query}': {e}")
            return ToolResult(success=False, message="An error occurred while trying to perform the web search.")
