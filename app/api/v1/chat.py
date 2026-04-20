from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatMessageRequest, ChatMessageResponse
from app.services.chat_service import send_chat_message

router = APIRouter()


@router.post("/message", response_model=ChatMessageResponse)
def post_message(payload: ChatMessageRequest) -> ChatMessageResponse:
    try:
        return send_chat_message(
            user_id=payload.user_id,
            message=payload.message,
            mode=payload.mode,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
