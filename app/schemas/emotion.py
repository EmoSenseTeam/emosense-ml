from __future__ import annotations

from pydantic import BaseModel, field_validator


class EmotionAnalysisRequest(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("text must not be empty")
        return normalized


class EmotionScores(BaseModel):
    positive: float
    neutral: float
    stress: float
    anxiety: float
    sad: float
    burnout: float


class EmotionAnalysisResponse(BaseModel):
    label: str
    confidence: float
    scores: EmotionScores
