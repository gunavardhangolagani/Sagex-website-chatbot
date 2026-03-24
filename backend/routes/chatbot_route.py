from fastapi import APIRouter, HTTPException
from models.chatbot_model import ChatRequest, ChatResponse
from controllers.chatbot_controller import help_fn_generate_chat_response
from models.chatbot_model import ChatRequest, ChatResponse
from controllers.chatbot_controller import help_fn_generate_chat_response

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint for RAG-based chatbot.

    - Accepts user question and optional chat history
    - Calls controller for processing
    - Returns structured response
    """
    try:
        result = help_fn_generate_chat_response(
            question=request.question,
            chat_history=[msg.dict() for msg in request.chat_history] if request.chat_history else []
        )

        return ChatResponse(
            answer=result.get("answer", ""),
            source=result.get("source", "")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
