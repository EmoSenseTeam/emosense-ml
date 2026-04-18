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

_DOMINANT_LABELS: dict[str, str] = {
    "sleep_deficit": "insufficient sleep",
    "screen_overuse": "excessive screen time",
    "high_anxiety": "elevated anxiety",
    "low_activity_risk": "sedentary behavior risk",
    "social_isolation_risk": "social isolation risk",
}


@lru_cache(maxsize=1)
def _load_model_bundle() -> dict[str, Any]:
    if not _MODEL_PATH.exists():
        raise FileNotFoundError(
            "Trained model not found at models/behavioral_model.pkl. "
            "Run first: python -m app.utils.prepare_dataset "
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
    if stress_score >= 75:
        return "critical"
    if stress_score >= 55:
        return "high"
    if stress_score >= 30:
        return "moderate"
    return "low"


def get_dominant_factor(
    daily_sleep_hours: float,
    screen_time_hours: float,
    anxiety_score: float,
    activity_risk_proxy: float,
    social_isolation_proxy: float,
) -> str:
    factors = {
        "sleep_deficit": max(0.0, 7.0 - daily_sleep_hours) * 10.0,
        "screen_overuse": max(0.0, screen_time_hours - 5.0) * 8.0,
        "high_anxiety": anxiety_score * 8.0,
        "low_activity_risk": activity_risk_proxy,
        "social_isolation_risk": social_isolation_proxy,
    }
    return max(factors, key=factors.get)


def build_summary(
    risk_level: str,
    dominant_factor: str,
    activity_risk_proxy: float,
    social_isolation_proxy: float,
) -> str:
    if risk_level == "low":
        base = (
            "Behavioral indicators are generally stable. "
            "No strong stress signals were detected."
        )
    else:
        label = _DOMINANT_LABELS.get(dominant_factor, dominant_factor)
        level_phrase = f"{risk_level.capitalize()} stress level detected. "
        base = (
            level_phrase
            + f"The dominant contributing factor is {label}."
        )
    extras: list[str] = []
    if activity_risk_proxy >= 60:
        extras.append(
            "Patterns also suggest possible low physical activity relative to screen and study load."
        )
    if social_isolation_proxy >= 60:
        extras.append(
            "Patterns also suggest possible social withdrawal or reduced offline engagement."
        )
    if extras:
        return base + " " + " ".join(extras)
    return base


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
        activity_risk,
        social_iso,
    )
    risk = get_risk_level(stress_score)
    summary = build_summary(risk, dominant, activity_risk, social_iso)

    return BehavioralAnalysisResponse(
        stress_score=stress_score,
        emotional_index=emotional_index,
        activity_risk_proxy=activity_risk,
        social_isolation_proxy=social_iso,
        dominant_factor=dominant,
        risk_level=risk,
        summary=summary,
    )
