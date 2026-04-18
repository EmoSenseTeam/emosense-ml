from fastapi import APIRouter, HTTPException

from app.schemas.behavioral import BehavioralAnalysisRequest, BehavioralAnalysisResponse
from app.services.behavioral_service import analyze_behavior

router = APIRouter()


@router.post("/analyze", response_model=BehavioralAnalysisResponse)
def post_analyze(payload: BehavioralAnalysisRequest) -> BehavioralAnalysisResponse:
    try:
        return analyze_behavior(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
