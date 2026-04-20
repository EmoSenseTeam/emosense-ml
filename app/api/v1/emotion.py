from fastapi import APIRouter, HTTPException

from app.schemas.emotion import EmotionAnalysisRequest, EmotionAnalysisResponse
from app.services.emotion_service import analyze_emotion

router = APIRouter()


@router.post("/analyze", response_model=EmotionAnalysisResponse)
def post_analyze(payload: EmotionAnalysisRequest) -> EmotionAnalysisResponse:
    try:
        return analyze_emotion(payload.text)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
