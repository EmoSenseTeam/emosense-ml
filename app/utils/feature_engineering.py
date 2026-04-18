from __future__ import annotations

from typing import Any, Mapping

_STRESS_LEVEL_SCORES: dict[str, float] = {
    "low": 30.0,
    "medium": 60.0,
    "high": 85.0,
}


def clamp(value: float, min_value: float = 0.0, max_value: float = 100.0) -> float:
    return max(min_value, min(max_value, value))


def create_stress_score(row: Mapping[str, Any]) -> float:
    anxiety = float(row["anxiety_score"])
    stress_level_raw = str(row["stress_level"]).strip().lower()
    mapped = _STRESS_LEVEL_SCORES.get(stress_level_raw)
    if mapped is None:
        raise ValueError(
            f"Unknown stress_level {stress_level_raw!r}; expected one of "
            f"{list(_STRESS_LEVEL_SCORES.keys())}"
        )
    stress_score = 0.6 * (anxiety * 10.0) + 0.4 * mapped
    return round(clamp(stress_score, 0.0, 100.0), 2)


def estimate_activity_risk_proxy(
    daily_sleep_hours: float,
    screen_time_hours: float,
    daily_study_hours: float,
    anxiety_score: float,
) -> float:
    score = 35.0
    if screen_time_hours > 8:
        score += 20.0
    elif screen_time_hours > 6:
        score += 10.0
    if daily_study_hours < 2:
        score += 10.0
    elif daily_study_hours > 10:
        score += 5.0
    if daily_sleep_hours > 9:
        score += 10.0
    elif daily_sleep_hours < 5:
        score += 10.0
    if anxiety_score >= 8:
        score += 20.0
    elif anxiety_score >= 6:
        score += 10.0
    return round(clamp(score, 0.0, 100.0), 2)


def estimate_social_isolation_proxy(
    screen_time_hours: float,
    anxiety_score: float,
    daily_sleep_hours: float,
    daily_study_hours: float,
) -> float:
    score = 30.0
    if screen_time_hours > 8:
        score += 15.0
    elif screen_time_hours > 6:
        score += 8.0
    if anxiety_score >= 8:
        score += 25.0
    elif anxiety_score >= 6:
        score += 12.0
    if daily_sleep_hours < 5:
        score += 10.0
    if daily_study_hours < 2:
        score += 8.0
    return round(clamp(score, 0.0, 100.0), 2)
