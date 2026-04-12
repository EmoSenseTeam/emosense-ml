"""Conversational emotion analysis — request/response schemas."""

from datetime import datetime

from pydantic import BaseModel, Field


class ConversationEmotionRequest(BaseModel):
    """Single message for emotion / stress inference (ML placeholder)."""

    user_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)
    context: str | None = Field(default=None, description="Optional dialogue or situational context")
    timestamp: datetime


class ConversationEmotionResponse(BaseModel):
    """Predicted emotion and stress indicators (to be filled by models later)."""

    emotion_label: str
    stress_probability: float = Field(..., ge=0.0, le=1.0)
    extracted_triggers: list[str] = Field(default_factory=list)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
