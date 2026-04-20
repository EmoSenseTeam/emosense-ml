from __future__ import annotations

from typing import Any

from pydantic import BaseModel, field_validator


class TextModerationRequest(BaseModel):
    user_id: int
    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("text must not be empty")
        return normalized


class TextModerationResponse(BaseModel):
    user_id: int
    final_label: str
    action: str
    confidence: float
    signals: dict[str, Any]
    reason: str
