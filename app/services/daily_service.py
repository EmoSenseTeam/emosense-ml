"""Daily aggregation — stub for future fusion logic."""

from app.schemas.daily import DailyAnalysisRequest, DailyAnalysisResponse


def analyze_daily(_payload: DailyAnalysisRequest) -> DailyAnalysisResponse:
    """Placeholder: combine behavioral + conversation signals into a daily index."""
    return DailyAnalysisResponse(
        daily_stress_index=0,
        main_factor="pending_implementation",
        short_recommendation="Daily fusion not yet implemented.",
    )
