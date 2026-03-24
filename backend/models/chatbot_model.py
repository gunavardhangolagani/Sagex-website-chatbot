from pydantic import BaseModel, Field
from typing import List, Optional


class ChatMessage(BaseModel):
    """
    Represents a single chat message in conversation history.
    """
    role: str = Field(..., description="Role of the sender: 'user' or 'model'")
    text: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """
    Incoming request schema for chatbot interaction.
    """
    question: str = Field(..., description="User query")
    chat_history: Optional[List[ChatMessage]] = Field(
        default=[],
        description="Previous conversation history"
    )


class ChatResponse(BaseModel):
    """
    Outgoing response schema from chatbot.
    """
    answer: str = Field(..., description="Generated answer")
    source: Optional[str] = Field(
        default="",
        description="Relevant source URL from knowledge base"
    )

