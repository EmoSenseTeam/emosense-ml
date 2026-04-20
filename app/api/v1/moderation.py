from fastapi import APIRouter, HTTPException

from app.schemas.moderation import TextModerationRequest, TextModerationResponse
from app.services.moderation_service import moderate_text

router = APIRouter()


@router.post("/text", response_model=TextModerationResponse)
def post_moderate_text(payload: TextModerationRequest) -> TextModerationResponse:
    try:
        result = moderate_text(user_id=payload.user_id, text=payload.text)
        return TextModerationResponse(**result)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
