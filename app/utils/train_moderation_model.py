from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline

_PROCESSED_PATH = Path("data/processed/moderation_dataset.csv")
_MODEL_PATH = Path("models/moderation_model.pkl")

_LABELS = [
    "toxic",
    "severe_toxic",
    "obscene",
    "threat",
    "insult",
    "identity_hate",
]


def main() -> None:
    if not _PROCESSED_PATH.exists():
        raise FileNotFoundError(
            f"{_PROCESSED_PATH} not found. Run: python -m app.utils.prepare_moderation_dataset"
        )

    df = pd.read_csv(_PROCESSED_PATH)
    missing = [c for c in ["text"] + _LABELS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    x = df["text"].astype(str)
    y = df[_LABELS].astype(int)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

    pipeline = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(max_features=20000, ngram_range=(1, 2)),
            ),
            (
                "clf",
                OneVsRestClassifier(
                    LogisticRegression(
                        max_iter=300,
                        class_weight="balanced",
                        random_state=42,
                        solver="saga",
                    ),
                    n_jobs=-1,
                ),
            ),
        ]
    )

    pipeline.fit(x_train, y_train)

    y_pred = pipeline.predict(x_test)
    print(classification_report(y_test, y_pred, target_names=_LABELS, zero_division=0))

    _MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    bundle = {"model": pipeline, "labels": _LABELS}
    joblib.dump(bundle, _MODEL_PATH)
    print(f"Saved model bundle to {_MODEL_PATH}")


if __name__ == "__main__":
    main()
