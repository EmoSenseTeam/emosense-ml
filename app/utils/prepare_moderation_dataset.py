from __future__ import annotations

from pathlib import Path

import pandas as pd

_RAW_PATH = Path("data/raw/toxic-comment-classification.csv")
_OUTPUT_PATH = Path("data/processed/moderation_dataset.csv")

_COLUMNS = [
    "comment_text",
    "toxic",
    "severe_toxic",
    "obscene",
    "threat",
    "insult",
    "identity_hate",
]

_LABELS = [
    "toxic",
    "severe_toxic",
    "obscene",
    "threat",
    "insult",
    "identity_hate",
]


def main() -> None:
    if not _RAW_PATH.exists():
        raise FileNotFoundError(
            f"Input dataset not found: {_RAW_PATH}. "
            "Place toxic-comment-classification.csv under data/raw/."
        )

    df = pd.read_csv(_RAW_PATH, usecols=_COLUMNS, low_memory=False)
    df = df.rename(columns={"comment_text": "text"})

    df["text"] = df["text"].astype("string").fillna("")
    df["text"] = df["text"].map(lambda x: str(x).strip())
    df = df[df["text"] != ""]
    df = df.dropna(subset=["text"])

    for col in _LABELS:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
        df[col] = df[col].clip(0, 1)

    df = df.dropna(how="any", subset=["text"] + _LABELS)

    _OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(_OUTPUT_PATH, index=False)
    print(f"Saved {len(df)} rows to {_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
