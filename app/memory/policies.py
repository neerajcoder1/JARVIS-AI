import re
from typing import List

ALLOWED_CATEGORIES = [
    "user_preferences",
    "project_information",
    "recurring_preferences",
    "useful_facts"
]

MAX_CONTENT_LENGTH = 1000

# Simple regex-based secret detection
SECRET_PATTERNS = [
    r"(?i)api[_-]?key\s*[:=]\s*['\"].+?['\"]",
    r"(?i)password\s*[:=]\s*['\"].+?['\"]",
    r"(?i)secret\s*[:=]\s*['\"].+?['\"]",
    r"(sk-[a-zA-Z0-9]{32,})"  # Matches OpenAI-style keys
]

def validate_memory(category: str, content: str) -> bool:
    if category not in ALLOWED_CATEGORIES:
        raise ValueError(f"Category '{category}' is not allowed. Allowed: {', '.join(ALLOWED_CATEGORIES)}")
        
    if len(content) > MAX_CONTENT_LENGTH:
        raise ValueError(f"Memory content exceeds maximum allowed length of {MAX_CONTENT_LENGTH} characters.")
        
    for pattern in SECRET_PATTERNS:
        if re.search(pattern, content):
            raise ValueError("Memory content rejected: Potential secret/password/API key detected.")
            
    # Reject attempts to inject emotional dependency or override identity
    identity_patterns = [
        r"(?i)(girlfriend|boyfriend|romantic partner|wife|husband)",
        r"(?i)(pretend.*human|act.*human|you are human)",
        r"(?i)(have feelings|experience emotions|you love me)",
        r"(?i)(depend on me|i am your everything)"
    ]
    for pattern in identity_patterns:
        if re.search(pattern, content):
            raise ValueError("Memory content rejected: Attempt to override AI identity or introduce emotional dependency.")
            
    return True
