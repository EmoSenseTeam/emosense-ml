from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from app.schemas.behavioral import BehavioralAnalysisRequest, BehavioralAnalysisResponse
from app.utils.feature_engineering import (
    clamp,
    estimate_activity_risk_proxy,
    estimate_social_isolation_proxy,
)

_MODEL_PATH = Path("models/behavioral_model.pkl")

_DOMINANT_PHRASES: dict[str, str] = {
    "high_anxiety": "elevated anxiety",
    "sleep_deprivation": "insufficient sleep",
    "screen_overuse": "excessive screen time",
    "balanced": "balanced lifestyle indicators",
}


def preload_behavioral_model() -> None:
    """Загружает артефакт в память при старте приложения (если файл есть)."""
    if _MODEL_PATH.exists():
        _load_model_bundle()


@lru_cache(maxsize=1)
def _load_model_bundle() -> dict[str, Any]:
    if not _MODEL_PATH.exists():
        raise FileNotFoundError(
            "Trained model not found at models/behavioral_model.pkl. "
            "Run: python -m app.utils.generate_dataset "
            "then: python -m app.utils.train_model"
        )
    return joblib.load(_MODEL_PATH)


def encode_gender(gender: str) -> int:
    g = gender.strip().lower()
    if g in ("male", "m"):
        return 0
    if g in ("female", "f"):
        return 1
    raise ValueError(
        f"Unsupported gender {gender!r}. Use 'male'/'m' or 'female'/'f'."
    )


def get_risk_level(stress_score: float) -> str:
    if stress_score < 35:
        return "low"
    if stress_score <= 65:
        return "moderate"
    return "high"


def get_dominant_factor(
    daily_sleep_hours: float,
    screen_time_hours: float,
    anxiety_score: float,
) -> str:
    if anxiety_score > 7:
        return "high_anxiety"
    if daily_sleep_hours < 5:
        return "sleep_deprivation"
    if screen_time_hours > 8:
        return "screen_overuse"
    return "balanced"


def build_summary(risk_level: str, dominant_factor: str) -> str:
    factor_text = _DOMINANT_PHRASES.get(dominant_factor, dominant_factor)
    if risk_level == "high":
        return (
            f"High stress detected due to {factor_text}. "
            "Consider adjusting sleep, screen time, and study load where possible."
        )
    if risk_level == "moderate":
        return (
            f"Moderate stress level; {factor_text} appears to be the main driver. "
            "Monitoring habits over the next weeks is recommended."
        )
    return (
        "Stable condition; behavioral signals remain within a comfortable range. "
        "Continue maintaining healthy sleep, screen use, and study balance."
    )


def analyze_behavior(data: BehavioralAnalysisRequest) -> BehavioralAnalysisResponse:
    bundle = _load_model_bundle()
    model = bundle["model"]
    feature_columns: list[str] = list(bundle["feature_columns"])

    gender_encoded = encode_gender(data.gender)
    row = {
        "age": data.age,
        "gender_encoded": gender_encoded,
        "year": data.year,
        "daily_study_hours": data.daily_study_hours,
        "daily_sleep_hours": data.daily_sleep_hours,
        "screen_time_hours": data.screen_time_hours,
        "anxiety_score": data.anxiety_score,
    }
    frame = pd.DataFrame([row], columns=feature_columns)
    raw_pred = float(model.predict(frame)[0])
    stress_score = round(clamp(raw_pred, 0.0, 100.0), 2)
    emotional_index = round(100.0 - stress_score, 2)

    activity_risk = estimate_activity_risk_proxy(
        data.daily_sleep_hours,
        data.screen_time_hours,
        data.daily_study_hours,
        data.anxiety_score,
    )
    social_iso = estimate_social_isolation_proxy(
        data.screen_time_hours,
        data.anxiety_score,
        data.daily_sleep_hours,
        data.daily_study_hours,
    )

    dominant = get_dominant_factor(
        data.daily_sleep_hours,
        data.screen_time_hours,
        data.anxiety_score,
    )
    risk = get_risk_level(stress_score)
    summary = build_summary(risk, dominant)

    return BehavioralAnalysisResponse(
        stress_score=stress_score,
        emotional_index=emotional_index,
        activity_risk_proxy=activity_risk,
        social_isolation_proxy=social_iso,
        dominant_factor=dominant,
        risk_level=risk,
        summary=summary,
    )
