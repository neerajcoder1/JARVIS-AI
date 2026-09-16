import os
from pathlib import Path
from typing import List, Optional
from app.core.config import settings
from app.filesystem.errors import PathOutsideSandboxError, SensitiveFileError

SENSITIVE_FILES = {
    ".env", ".env.local", ".env.development", ".env.test", ".env.production",
    "credentials.json", "secrets.json", "secret.json",
    "id_rsa", "id_ed25519", "id_ecdsa", "id_dsa"
}
SENSITIVE_EXTENSIONS = {
    ".pem", ".key", ".p12", ".pfx", ".pub"
}
SENSITIVE_DIRS = {
    ".ssh", ".aws", ".azure", ".config/gcloud", ".kube"
}

class FilesystemSandbox:
    def __init__(self):
        self._roots: List[Path] = []
        self._initialize_roots()

    def _initialize_roots(self) -> None:
        if settings.FILESYSTEM_ALLOWED_ROOTS:
            paths = settings.FILESYSTEM_ALLOWED_ROOTS.split(",")
            for p in paths:
                p = p.strip()
                if p:
                    try:
                        resolved = Path(p).resolve(strict=True)
                        self._roots.append(resolved)
                    except Exception:
                        pass
        
        # If no roots configured, provide safe defaults: project dir, Desktop, Documents
        if not self._roots:
            self._roots.append(Path.cwd().resolve())
            try:
                self._roots.append((Path.home() / "Desktop").resolve())
                self._roots.append((Path.home() / "Documents").resolve())
            except Exception:
                pass

    def get_roots(self) -> List[Path]:
        return self._roots

    def validate_path(self, path_str: str) -> Path:
        """
        Resolves the path and ensures it lies within an approved root.
        Raises PathOutsideSandboxError if invalid.
        """
        try:
            # We use strict=False because the path might be to a new file, but wait, this is read-only
            # so strict=False is fine to just resolve the absolute path string.
            requested_path = Path(path_str).resolve()
        except Exception as e:
            raise PathOutsideSandboxError(f"Invalid path format: {e}")

        # Check against approved roots
        is_approved = False
        for root in self._roots:
            try:
                if requested_path.is_relative_to(root):
                    is_approved = True
                    break
            except AttributeError:
                # Python < 3.9 fallback, though we are on 3.12
                try:
                    requested_path.relative_to(root)
                    is_approved = True
                    break
                except ValueError:
                    pass

        if not is_approved:
            raise PathOutsideSandboxError("The requested path is outside the approved filesystem sandbox.")

        self._check_sensitive(requested_path)
        return requested_path

    def _check_sensitive(self, path: Path) -> None:
        # Check filename
        if path.name.lower() in SENSITIVE_FILES:
            raise SensitiveFileError("Access to this sensitive file is forbidden.")
        
        # Check extension
        if path.suffix.lower() in SENSITIVE_EXTENSIONS:
            raise SensitiveFileError("Access to this sensitive file type is forbidden.")
            
        # Check parent directories
        for part in path.parts:
            if part.lower() in SENSITIVE_DIRS:
                raise SensitiveFileError("Access to this sensitive directory is forbidden.")

sandbox = FilesystemSandbox()
