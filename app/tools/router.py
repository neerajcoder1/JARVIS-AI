import re
from typing import List

# Tool categories mapping
TOOL_GROUPS = {
    "APPLICATION": [
        "open_application",
        "close_application"
    ],
    "SYSTEM": [
        "get_system_info",
        "get_current_time"
    ],
    "BROWSER": [
        "open_website",
        "search_web",
        "browser_open",
        "browser_get_page_title",
        "browser_read_page",
        "browser_get_links",
        "browser_close"
    ],
    "FILESYSTEM_READ": [
        "filesystem_list",
        "filesystem_read_text",
        "filesystem_find",
        "filesystem_get_metadata"
    ],
    "FILESYSTEM_WRITE": [
        "filesystem_create_file",
        "filesystem_write_text",
        "filesystem_append_text",
        "filesystem_create_directory",
        "filesystem_copy",
        "filesystem_move",
        "filesystem_delete"
    ],
    "MEMORY": [
        "save_memory",
        "retrieve_memory",
        "delete_memory",
        "update_memory"
    ],
    "SCREEN": [
        "inspect_screen"
    ],
    "INPUT": [
        "mouse_move",
        "mouse_click",
        "keyboard_type",
        "keyboard_press"
    ]
}

def route_tools(query: str) -> List[str]:
    """
    Returns a list of tool names that are contextually relevant to the user's query.
    This prevents sending 22 tools (and ~2000 tokens) to the LLM on every request.
    """
    if not query:
        return []
        
    query_lower = query.lower()
    selected_tools = set()

    # SYSTEM Routing
    if re.search(r'\b(time|date|system info|os|cpu|memory|system|samay|waqt|baj|baje)\b', query_lower):
        selected_tools.update(TOOL_GROUPS["SYSTEM"])

    # BROWSER Routing
    if re.search(r'\b(browser|website|google|search|url|http|https|page|web|webpage|read page|links|open (google|youtube|website)|kholo|khulo|dhundo|search karo|read karo)\b', query_lower):
        selected_tools.update(TOOL_GROUPS["BROWSER"])

    # APPLICATION Routing
    if re.search(r'\b(open|close|launch|start|quit|run|band karo|kholo|chalu karo)\b', query_lower):
        selected_tools.update(TOOL_GROUPS["APPLICATION"])

    # FILESYSTEM READ Routing
    if re.search(r'\b(list|read|show files|find|metadata|desktop|documents|folder|directory|files|file|dikhao|kaha hai|padho|check karo)\b', query_lower):
        selected_tools.update(TOOL_GROUPS["FILESYSTEM_READ"])

    # FILESYSTEM WRITE Routing
    if re.search(r'\b(create|write|append|make|copy|move|delete|remove|mkdir|banao|likho|hatao|delete karo|copy karo)\b', query_lower):
        selected_tools.update(TOOL_GROUPS["FILESYSTEM_WRITE"])

    # MEMORY Routing
    if re.search(r'\b(remember|memory|forget|project|preferences|what did i tell you|recall|save|yaad|yaad rakho|bhul jao)\b', query_lower):
        selected_tools.update(TOOL_GROUPS["MEMORY"])

    # SCREEN Routing
    if re.search(r'\b(screen|read this|what is on|inspect|screenshot|error|what does .* say|dekho)\b', query_lower):
        selected_tools.update(TOOL_GROUPS["SCREEN"])

    # INPUT Routing
    if re.search(r'\b(click|type|press|enter|mouse|keyboard|scroll|cursor|dabao|likho)\b', query_lower):
        selected_tools.update(TOOL_GROUPS["INPUT"])

    # If the user says "test.txt", they might just mention a file without action words, but we captured 'file' or action words.
    
    return list(selected_tools)
