from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, field_validator


class ChatMessageRequest(BaseModel):
    user_id: int
    message: str
    mode: Literal["soft", "strict"]

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("message must not be empty")
        return normalized


class ChatEmotionResult(BaseModel):
    label: str
    confidence: float


class ChatMessageResponse(BaseModel):
    reply: str
    mode: Literal["soft", "strict"]
    emotion: ChatEmotionResult
    history_length: int
