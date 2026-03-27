from pydantic import BaseModel

class ChatbotRequestConversationHistory(BaseModel):
    role: str
    content: str

class ChatbotRequest(BaseModel):
    message: str
    conversation_history: list[ChatbotRequestConversationHistory]

class ChatbotResponse(BaseModel):
    message: str