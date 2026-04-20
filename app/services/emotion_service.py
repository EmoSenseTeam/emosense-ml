from __future__ import annotations

from typing import Any

from app.schemas.emotion import EmotionAnalysisResponse, EmotionScores
from app.services.ai_client import analyze_emotion_with_ai

ALLOWED_EMOTION_LABELS: set[str] = {
    "positive",
    "neutral",
    "stress",
    "anxiety",
    "sad",
    "burnout",
}
EMOTION_LABEL_ORDER: tuple[str, ...] = (
    "positive",
    "neutral",
    "stress",
    "anxiety",
    "sad",
    "burnout",
)

emotion_history: list[dict[str, str | float]] = []


def _clamp_score(value: float) -> float:
    return max(0.0, min(1.0, value))


def _to_float(value: Any, field_name: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be numeric") from exc


def analyze_emotion(text: str) -> EmotionAnalysisResponse:
    ai_result = analyze_emotion_with_ai(text)

    label = str(ai_result.get("label", "")).strip().lower()
    if label not in ALLOWED_EMOTION_LABELS:
        raise ValueError(
            f"Invalid emotion label: {label!r}. Allowed labels: {sorted(ALLOWED_EMOTION_LABELS)}"
        )

    confidence_raw = _to_float(ai_result.get("confidence"), "confidence")
    confidence = _clamp_score(confidence_raw)

    scores_data = ai_result.get("scores")
    if not isinstance(scores_data, dict):
        raise ValueError("scores must be an object")

    normalized_scores: dict[str, float] = {}
    for emotion_label in EMOTION_LABEL_ORDER:
        if emotion_label not in scores_data:
            raise ValueError(f"scores.{emotion_label} is required")
        normalized_scores[emotion_label] = _clamp_score(
            _to_float(scores_data[emotion_label], f"scores.{emotion_label}")
        )

    scores = EmotionScores(**normalized_scores)
    response = EmotionAnalysisResponse(
        label=label,
        confidence=confidence,
        scores=scores,
    )
    emotion_history.append(
        {
            "text": text,
            "label": response.label,
            "confidence": response.confidence,
        }
    )
    return response
