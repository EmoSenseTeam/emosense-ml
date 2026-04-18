from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

from app.utils.feature_engineering import create_stress_score

# Primary input CSV path. Change INPUT_PATH if your file has another name
# (e.g. "data/raw/student_mental_health_burnout.csv") or place a copy at dataset.csv.
INPUT_PATH = "data/raw/dataset.csv"
_FALLBACK_INPUT = "data/raw/student_mental_health_burnout.csv"

_REQUIRED_COLUMNS = [
    "student_id",
    "age",
    "gender",
    "course",
    "year",
    "daily_study_hours",
    "daily_sleep_hours",
    "screen_time_hours",
    "stress_level",
    "anxiety_score",
]

_GENDER_MAP = {"male": 0, "female": 1}
_STRESS_MAP = {"low": 0, "medium": 1, "high": 2}

_OUTPUT_COLUMNS = [
    "age",
    "gender_encoded",
    "year",
    "daily_study_hours",
    "daily_sleep_hours",
    "screen_time_hours",
    "anxiety_score",
    "stress_level_encoded",
    "stress_score",
    "emotional_index",
]


def _resolve_input_path() -> Path:
    primary = Path(INPUT_PATH)
    if primary.exists():
        return primary
    fallback = Path(_FALLBACK_INPUT)
    if fallback.exists():
        print(
            f"Note: {primary} not found; using {fallback}. "
            "Copy or rename your CSV to dataset.csv if you want a fixed filename.",
            file=sys.stderr,
        )
        return fallback
    raise FileNotFoundError(
        f"Input CSV not found: {primary}. "
        "Create the file or set INPUT_PATH in this module to an existing CSV."
    )


def parse_year_to_int(value: object) -> int:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        raise ValueError("year value is missing")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if float(value).is_integer():
            y = int(value)
            if 1 <= y <= 6:
                return y
        raise ValueError(f"year numeric out of range 1..6: {value!r}")
    s = str(value).strip().lower()
    if s.isdigit():
        y = int(s)
        if 1 <= y <= 6:
            return y
        raise ValueError(f"year numeric out of range 1..6: {value!r}")
    m = re.match(r"^(\d+)(st|nd|rd|th)$", s)
    if m:
        y = int(m.group(1))
        if 1 <= y <= 6:
            return y
    raise ValueError(f"Cannot parse academic year from value: {value!r}")


def _encode_gender_series(normalized: pd.Series) -> pd.Series:
    allowed = set(_GENDER_MAP)
    unknown = sorted({g for g in normalized.unique() if g not in allowed and pd.notna(g)})
    if unknown:
        raise ValueError(
            "Unknown gender value(s) after normalization: "
            f"{unknown!r}. Expected only {sorted(allowed)!r}."
        )
    return normalized.map(_GENDER_MAP).astype(int)


def _encode_stress_series(normalized: pd.Series) -> pd.Series:
    allowed = set(_STRESS_MAP)
    unknown = sorted({g for g in normalized.unique() if g not in allowed and pd.notna(g)})
    if unknown:
        raise ValueError(
            "Unknown stress_level value(s) after normalization: "
            f"{unknown!r}. Expected only {sorted(allowed)!r}."
        )
    return normalized.map(_STRESS_MAP).astype(int)


def main() -> None:
    input_path = _resolve_input_path()
    df = pd.read_csv(input_path)

    missing = [c for c in _REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df[_REQUIRED_COLUMNS].copy()
    df["gender"] = df["gender"].astype(str).str.strip().str.lower()
    df["stress_level"] = df["stress_level"].astype(str).str.strip().str.lower()
    df["course"] = df["course"].astype(str).str.strip()

    before = len(df)
    df = df[df["gender"].isin(_GENDER_MAP)].copy()
    dropped = before - len(df)
    if dropped:
        print(
            f"Warning: dropped {dropped} row(s) with gender not in {list(_GENDER_MAP)} "
            "(only male/female are used for training).",
            file=sys.stderr,
        )
    if df.empty:
        raise ValueError("No rows left after filtering genders; cannot build dataset.")

    df["year"] = df["year"].apply(parse_year_to_int)

    df["stress_score"] = df.apply(create_stress_score, axis=1)
    df["emotional_index"] = 100.0 - df["stress_score"]

    df["gender_encoded"] = _encode_gender_series(df["gender"])
    df["stress_level_encoded"] = _encode_stress_series(df["stress_level"])

    out = df[_OUTPUT_COLUMNS].copy()
    out_dir = Path("data/processed")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "clean_data.csv"
    out.to_csv(out_path, index=False)
    print(f"Wrote {out_path} ({len(out)} rows).")


if __name__ == "__main__":
    main()
