class FilesystemError(Exception):
    """Base class for filesystem-related errors."""
    pass

class PathOutsideSandboxError(FilesystemError):
    """Raised when an operation attempts to access a path outside the approved roots."""
    pass

class SensitiveFileError(FilesystemError):
    """Raised when attempting to access a forbidden or sensitive file."""
    pass

class UnsupportedFileTypeError(FilesystemError):
    """Raised when attempting to read a file with an unsupported extension."""
    pass
