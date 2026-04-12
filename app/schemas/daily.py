"""Daily aggregated analysis — nested request/response schemas."""

from pydantic import BaseModel, Field

from app.schemas.behavioral import BehavioralAnalysisResponse
from app.schemas.conversation import ConversationEmotionResponse


class DailyAnalysisRequest(BaseModel):
    """Combines behavioral and conversational module outputs for one day."""

    user_id: str = Field(..., min_length=1)
    behavioral_result: BehavioralAnalysisResponse = Field(
        ...,
        description="Output of the behavioral analysis module",
    )
    conversation_result: ConversationEmotionResponse = Field(
        ...,
        description="Output of the conversational emotion module",
    )


class DailyAnalysisResponse(BaseModel):
    """Daily stress summary (aggregation logic TBD)."""

    daily_stress_index: int = Field(..., ge=0, le=100)
    main_factor: str
    short_recommendation: str
