class BrowserError(Exception):
    """Base class for browser-related errors."""
    pass

class BrowserNotRunningError(BrowserError):
    """Raised when an operation requires an active browser session, but none exists."""
    pass
