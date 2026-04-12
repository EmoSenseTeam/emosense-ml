"""Deep / longitudinal analysis — request/response schemas."""

from typing import Any

from pydantic import BaseModel, Field


class DeepAnalysisRequest(BaseModel):
    """
    Multi-period deep analysis input.

    History fields are intentionally flexible dicts for MVP;
    replace with typed models when pipelines stabilize.
    """

    user_id: str = Field(..., min_length=1)
    period: str = Field(..., description="e.g. week, month, semester")
    daily_history: list[dict[str, Any]] = Field(default_factory=list)
    behavioral_history: list[dict[str, Any]] = Field(default_factory=list)
    conversation_history: list[dict[str, Any]] = Field(default_factory=list)


class DeepAnalysisResponse(BaseModel):
    """Trends, correlations, and narrative summary (ML placeholder)."""

    period: str
    trend: str
    average_stress_index: float
    top_factors: list[str] = Field(default_factory=list)
    correlations: dict[str, float] = Field(default_factory=dict)
    summary: str
