from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

_PROCESSED_PATH = Path("data/processed/better_data.csv")
_MODEL_PATH = Path("models/behavioral_model.pkl")

_FEATURE_COLUMNS = [
    "age",
    "gender_encoded",
    "year",
    "daily_study_hours",
    "daily_sleep_hours",
    "screen_time_hours",
    "anxiety_score",
]

_TARGET_COLUMN = "stress_score"


def main() -> None:
    if not _PROCESSED_PATH.exists():
        raise FileNotFoundError(
            f"{_PROCESSED_PATH} not found. Run: python -m app.utils.generate_dataset"
        )

    df = pd.read_csv(_PROCESSED_PATH)
    missing = [c for c in _FEATURE_COLUMNS + [_TARGET_COLUMN] if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in processed data: {missing}")

    x = df[_FEATURE_COLUMNS]
    y = df[_TARGET_COLUMN]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=12,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(x_train, y_train)
    pred = model.predict(x_test)

    mae = mean_absolute_error(y_test, pred)
    r2 = r2_score(y_test, pred)
    print(f"mean_absolute_error: {mae:.4f}")
    print(f"r2_score: {r2:.4f}")

    importance = pd.DataFrame(
        {"feature": _FEATURE_COLUMNS, "importance": model.feature_importances_}
    ).sort_values("importance", ascending=False)
    print(importance.to_string(index=False))

    _MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    bundle = {"model": model, "feature_columns": _FEATURE_COLUMNS}
    joblib.dump(bundle, _MODEL_PATH)
    print(f"Saved model bundle to {_MODEL_PATH}")


if __name__ == "__main__":
    main()
