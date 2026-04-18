from pydantic import BaseModel, Field


class BehavioralAnalysisRequest(BaseModel):
    age: int = Field(ge=15, le=40)
    gender: str
    year: int = Field(ge=1, le=6)
    daily_study_hours: float = Field(ge=0, le=24)
    daily_sleep_hours: float = Field(ge=0, le=24)
    screen_time_hours: float = Field(ge=0, le=24)
    anxiety_score: float = Field(ge=1, le=10)


class BehavioralAnalysisResponse(BaseModel):
    stress_score: float
    emotional_index: float
    activity_risk_proxy: float
    social_isolation_proxy: float
    dominant_factor: str
    risk_level: str
    summary: str
