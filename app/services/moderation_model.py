from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib

_MODEL_PATH = Path("models/moderation_model.pkl")


@lru_cache(maxsize=1)
def _load_bundle() -> dict[str, Any]:
    if not _MODEL_PATH.exists():
        raise RuntimeError(
            f"Moderation model not found at {_MODEL_PATH}. "
            "Run: python -m app.utils.prepare_moderation_dataset && "
            "python -m app.utils.train_moderation_model"
        )
    bundle = joblib.load(_MODEL_PATH)
    if not isinstance(bundle, dict) or "model" not in bundle or "labels" not in bundle:
        raise RuntimeError("Invalid moderation model bundle format.")
    return bundle


def predict_signals(text: str) -> dict[str, float]:
    bundle = _load_bundle()
    model = bundle["model"]
    labels: list[str] = list(bundle["labels"])

    probs = model.predict_proba([text])
    if probs.ndim != 2:
        raise RuntimeError("Unexpected predict_proba output shape.")

    if probs.shape[1] != len(labels):
        raise RuntimeError(
            f"Label count mismatch: got {probs.shape[1]} columns, expected {len(labels)}"
        )

    row = probs[0]
    return {label: float(row[i]) for i, label in enumerate(labels)}
