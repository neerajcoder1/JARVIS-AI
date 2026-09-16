from app.core.config import settings
from app.core.logger import logger
from app.core.exceptions import AIError
from app.brain.prompts import get_system_prompt
from app.brain.memory import ShortTermMemory

class AIEngine:
    def __init__(self):
        from app.brain.providers import get_provider
        self.provider = get_provider()
        self.system_prompt = get_system_prompt()
        self.memory = ShortTermMemory()

    def generate_response(self, user_text: str) -> str:
        if not user_text:
            return ""
            
        try:
            logger.info("Generating response...")
            
            from app.tools.executor import ToolExecutor
            from app.tools.router import route_tools
            import json
            
            # If we have a pending tool call, process confirmation
            if hasattr(self, 'pending_tool_call') and self.pending_tool_call:
                import re
                clean_text = re.sub(r'[^a-zA-Z0-9]', '', user_text.lower())
                if clean_text in ["yes", "y", "sure", "ok", "okay", "doit", "continue", "yep", "yeah", "yesproceed", "confirm"]:
                    logger.info("User confirmed tool execution.")
                    success, msg, data = ToolExecutor.handle_tool_call(
                        self.pending_tool_call["name"],
                        self.pending_tool_call["arguments"],
                        user_confirmed=True
                    )
                    
                    assistant_msg = self.pending_tool_call["assistant_message"]
                    tool_id = self.pending_tool_call["tool_call_id"]
                    allowed_tools = self.pending_tool_call.get("allowed_tools", [])
                    self.pending_tool_call = None
                    
                    messages = [{"role": "system", "content": self.system_prompt}]
                    messages.extend(self.memory.get_messages())
                    
                    # Add user's "Yes"
                    messages.append({"role": "user", "content": user_text})
                    
                    # Add the original assistant tool call
                    messages.append(assistant_msg)
                    
                    # Add the tool result
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_id,
                        "content": f"Result: {msg}"
                    })
                    
                    # Only send tools relevant to the initial request
                    tools = ToolExecutor.get_openai_tools(allowed_names=allowed_tools)
                    
                    response = self.provider.generate_response(
                        messages=messages,
                        tools=tools if tools else None
                    )
                    ai_text = response.choices[0].message.content.strip()
                    
                    self.memory.add_message("user", user_text)
                    self.memory.add_message("assistant", ai_text)
                    return ai_text
                else:
                    self.pending_tool_call = None
                    logger.info("User denied tool execution.")
                    self.memory.add_message("user", user_text)
                    self.memory.add_message("assistant", "Action cancelled.")
                    return "Action cancelled."

            # Normal flow
            messages = [{"role": "system", "content": self.system_prompt}]
            messages.extend(self.memory.get_messages())
            messages.append({"role": "user", "content": user_text})
            
            allowed_tools = route_tools(user_text)
            tools = ToolExecutor.get_openai_tools(allowed_names=allowed_tools)
            
            response = self.provider.generate_response(
                messages=messages,
                tools=tools if tools else None
            )
            
            message = response.choices[0].message
            
            if getattr(message, "tool_calls", None):
                # Handle first tool call
                tool_call = message.tool_calls[0]
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                
                success, msg, data = ToolExecutor.handle_tool_call(tool_name, arguments, user_confirmed=False)
                
                if data == "NEEDS_CONFIRMATION":
                    self.pending_tool_call = {
                        "name": tool_name,
                        "arguments": arguments,
                        "tool_call_id": tool_call.id,
                        "assistant_message": message.model_dump(exclude_none=True),
                        "allowed_tools": allowed_tools
                    }
                    return msg
                else:
                    # Tool executed immediately (SAFE) or was denied (RESTRICTED)
                    
                    # 1. Add the assistant's tool call message
                    self.memory.add_message("assistant", message.content or "")
                    
                    # 2. To strictly comply with OpenAI standard, we shouldn't save these temporary tool states to short-term text memory
                    # Instead, we just pass them directly to the API for the final generation
                    temp_messages = list(messages)
                    temp_messages.append(message.model_dump(exclude_none=True))
                    temp_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": f"Result: {msg}"
                    })
                    
                    final_response = self.provider.generate_response(
                        messages=temp_messages
                    )
                    ai_text = final_response.choices[0].message.content.strip()
                    
                    self.memory.add_message("user", user_text)
                    self.memory.add_message("assistant", ai_text)
                    return ai_text
            
            # No tool call
            ai_text = message.content.strip()
            self.memory.add_message("user", user_text)
            self.memory.add_message("assistant", ai_text)
            
            logger.info("AI response generated")
            return ai_text
            
        except getattr(__import__('app.core.exceptions', fromlist=['AIRateLimitError']), 'AIRateLimitError') as e:
            raise e
        except Exception as e:
            logger.error(f"AI API failure: {e}")
            raise AIError(f"Failed to generate response: {e}")
            
    def clear_memory(self):
        self.memory.clear()
