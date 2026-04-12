"""Rule-based behavioral scoring (MVP baseline, replaceable by ML later)."""

from app.schemas.behavioral import BehavioralAnalysisRequest, BehavioralAnalysisResponse
from app.utils.helpers import clamp_int


def _risk_level_from_index(index: int) -> str:
    """Map emotional index to qualitative risk band."""
    if index <= 39:
        return "high"
    if index <= 69:
        return "moderate"
    return "low"


def analyze_behavioral(payload: BehavioralAnalysisRequest) -> BehavioralAnalysisResponse:
    """
    Compute emotional_index from lifestyle signals using fixed rules.

    Starts at 100 and applies penalties; result is clamped to [0, 100].
    """
    score = 100

    # Sleep
    if payload.sleep_hours < 6:
        score -= 20
    if payload.sleep_hours < 4:
        score -= 10  # stronger penalty for severe sleep deficit

    # Screen time
    if payload.screen_time_hours > 8:
        score -= 15
    if payload.screen_time_hours > 10:
        score -= 10  # extra penalty for very high use

    # Activity & social
    if payload.physical_activity_steps < 5000:
        score -= 10
    if payload.communication_frequency < 3:
        score -= 10

    emotional_index = clamp_int(score, 0, 100)
    risk = _risk_level_from_index(emotional_index)

    signals: list[str] = []
    if payload.sleep_hours < 6:
        signals.append("low_sleep")
    if payload.screen_time_hours > 8:
        signals.append("high_screen_time")
    if payload.physical_activity_steps < 5000:
        signals.append("low_physical_activity")
    if payload.communication_frequency < 3:
        signals.append("low_communication")

    return BehavioralAnalysisResponse(
        emotional_index=emotional_index,
        risk_level=risk,
        main_behavioral_signals=signals,
    )
