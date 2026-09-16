import tiktoken
import json
from app.brain.prompts import get_system_prompt
from app.brain.llm import AIEngine
from app.tools.executor import ToolExecutor
from app.tools.registry import registry
from app.tools.applications import OpenApplicationTool, CloseApplicationTool
from app.tools.system_info import GetSystemInfoTool
from app.tools.time_tool import GetCurrentTimeTool
from app.tools.browser import OpenWebsiteTool, SearchWebTool
from app.tools.controlled_browser import BrowserOpenTool, BrowserGetPageTitleTool, BrowserReadPageTool, BrowserGetLinksTool, BrowserCloseTool
from app.tools.filesystem import (
    FilesystemListTool, FilesystemReadTextTool, FilesystemFindTool, FilesystemGetMetadataTool,
    FilesystemCreateFileTool, FilesystemWriteTextTool, FilesystemAppendTextTool,
    FilesystemCreateDirectoryTool, FilesystemCopyTool, FilesystemMoveTool, FilesystemDeleteTool
)

enc = tiktoken.encoding_for_model("gpt-4")

def count_tokens(text: str) -> int:
    return len(enc.encode(text))

def get_tools_token_count():
    tools = ToolExecutor.get_openai_tools()
    return count_tokens(json.dumps(tools))

registry.register(OpenApplicationTool())
registry.register(CloseApplicationTool())
registry.register(GetSystemInfoTool())
registry.register(GetCurrentTimeTool())
registry.register(OpenWebsiteTool())
registry.register(SearchWebTool())
registry.register(BrowserOpenTool())
registry.register(BrowserGetPageTitleTool())
registry.register(BrowserReadPageTool())
registry.register(BrowserGetLinksTool())
registry.register(BrowserCloseTool())
registry.register(FilesystemListTool())
registry.register(FilesystemReadTextTool())
registry.register(FilesystemFindTool())
registry.register(FilesystemGetMetadataTool())
registry.register(FilesystemCreateFileTool())
registry.register(FilesystemWriteTextTool())
registry.register(FilesystemAppendTextTool())
registry.register(FilesystemCreateDirectoryTool())
registry.register(FilesystemCopyTool())
registry.register(FilesystemMoveTool())
registry.register(FilesystemDeleteTool())

sys_prompt = get_system_prompt()
sys_tokens = count_tokens(sys_prompt)
tool_tokens = get_tools_token_count()

from app.tools.router import route_tools

print("------------------------------------------")
print("JARVIS TOKEN AUDIT (AFTER ROUTING)")
print("------------------------------------------")
print(f"Total registered tools: {len(registry._tools)}")
print(f"System prompt:          {sys_tokens}")
print(f"Tool definitions (all): {tool_tokens}")

queries = [
    ("TEST A", "What is Python?"),
    ("TEST B", "What is cybersecurity?"),
    ("TEST C", "Open Google."),
    ("TEST D", "Read the current webpage."),
    ("TEST E", "List the files on my Desktop."),
    ("TEST F", "Create test.txt on my Desktop.")
]

for name, q in queries:
    u_tok = count_tokens(q)
    allowed_names = route_tools(q)
    filtered_tools = ToolExecutor.get_openai_tools(allowed_names=allowed_names)
    filt_tool_tokens = count_tokens(json.dumps(filtered_tools)) if filtered_tools else 0
    print(f"\n{name} ('{q}')")
    print(f"User message:           {u_tok}")
    print(f"Routed Tools:           {len(filtered_tools)} tools ({filt_tool_tokens} tokens)")
    print(f"Estimated input:        {sys_tokens + filt_tool_tokens + u_tok}")
print("------------------------------------------")
