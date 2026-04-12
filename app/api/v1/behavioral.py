"""Behavioral analysis HTTP routes."""

from fastapi import APIRouter, status

from app.schemas.behavioral import BehavioralAnalysisRequest, BehavioralAnalysisResponse
from app.services import behavioral_service

router = APIRouter(tags=["behavioral"])


@router.post(
    "/behavioral",
    response_model=BehavioralAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Behavioral data analysis",
    description="Baseline rule-based emotional index from lifestyle signals.",
)
def post_behavioral_analysis(
    body: BehavioralAnalysisRequest,
) -> BehavioralAnalysisResponse:
    """Validate input and delegate scoring to the service layer."""
    return behavioral_service.analyze_behavioral(body)
