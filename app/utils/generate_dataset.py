from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

_OUTPUT_PATH = Path("data/processed/better_data.csv")
_N_ROWS = 250
_RNG = np.random.default_rng(42)


def main() -> None:
    n = _N_ROWS
    age = _RNG.integers(16, 41, size=n)
    gender_encoded = _RNG.integers(0, 2, size=n)
    year = _RNG.integers(1, 7, size=n)
    daily_study_hours = _RNG.uniform(1.0, 14.0, size=n)
    daily_sleep_hours = _RNG.uniform(4.0, 10.0, size=n)
    screen_time_hours = _RNG.uniform(1.0, 14.0, size=n)
    anxiety_score = _RNG.uniform(1.0, 10.0, size=n)

    noise = _RNG.uniform(-5.0, 5.0, size=n)
    stress_score = (
        anxiety_score * 5.5
        + (7.0 - daily_sleep_hours) * 3.5
        + screen_time_hours * 1.8
        + daily_study_hours * 1.2
        + noise
    )
    stress_score = np.clip(stress_score, 10.0, 100.0)
    emotional_index = 100.0 - stress_score

    stress_level_encoded = np.zeros(n, dtype=int)
    stress_level_encoded[(stress_score >= 35.0) & (stress_score <= 65.0)] = 1
    stress_level_encoded[stress_score > 65.0] = 2

    df = pd.DataFrame(
        {
            "age": age,
            "gender_encoded": gender_encoded,
            "year": year,
            "daily_study_hours": np.round(daily_study_hours, 2),
            "daily_sleep_hours": np.round(daily_sleep_hours, 2),
            "screen_time_hours": np.round(screen_time_hours, 2),
            "anxiety_score": np.round(anxiety_score, 2),
            "stress_level_encoded": stress_level_encoded,
            "stress_score": np.round(stress_score, 2),
            "emotional_index": np.round(emotional_index, 2),
        }
    )

    _OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(_OUTPUT_PATH, index=False)
    print(f"Saved {len(df)} rows to {_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
