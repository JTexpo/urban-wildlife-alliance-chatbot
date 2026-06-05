from pydantic import BaseModel


class ChatbotConversationContent(BaseModel):
    text: str


class ChatbotRequestConversationHistory(BaseModel):
    role: str
    content: list[ChatbotConversationContent]


class ChatbotRequest(BaseModel):
    message: str
    conversation_history: list[ChatbotRequestConversationHistory]


class ChatbotResponse(BaseModel):
    message: str
