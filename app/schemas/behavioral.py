"""Behavioral data analysis — request/response schemas."""

from pydantic import BaseModel, Field


class BehavioralAnalysisRequest(BaseModel):
    """Input payload for behavioral analysis."""

    user_id: str = Field(..., min_length=1, description="Stable user identifier")
    screen_time_hours: float = Field(..., ge=0.0, description="Average daily screen time in hours")
    sleep_hours: float = Field(..., ge=0.0, le=24.0, description="Average sleep duration in hours")
    physical_activity_steps: int = Field(..., ge=0, description="Daily step count")
    communication_frequency: int = Field(..., ge=0, description="Social interaction score / count")


class BehavioralAnalysisResponse(BaseModel):
    """Baseline behavioral scoring output."""

    emotional_index: int = Field(..., ge=0, le=100, description="Composite emotional wellbeing index")
    risk_level: str = Field(..., description="Qualitative risk band: high | moderate | low")
    main_behavioral_signals: list[str] = Field(
        default_factory=list,
        description="Detected behavioral risk signals",
    )
