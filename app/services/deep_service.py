"""Deep / longitudinal analysis — stub for future time-series & correlation models."""

from app.schemas.deep import DeepAnalysisRequest, DeepAnalysisResponse


def analyze_deep(_payload: DeepAnalysisRequest) -> DeepAnalysisResponse:
    """Placeholder: trends, correlations, and summaries over `period`."""
    return DeepAnalysisResponse(
        period=_payload.period,
        trend="stable",
        average_stress_index=0.0,
        top_factors=[],
        correlations={},
        summary="Deep analysis not yet implemented.",
    )
