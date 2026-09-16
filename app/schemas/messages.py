from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    
class ChatResponse(BaseModel):
    response: str
