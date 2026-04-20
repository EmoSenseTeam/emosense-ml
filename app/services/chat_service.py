from __future__ import annotations

from typing import Any

from app.schemas.chat import ChatEmotionResult, ChatMessageResponse
from app.services.ai_client import generate_chat_reply
from app.services.emotion_service import analyze_emotion

chat_history_store: dict[int, list[dict[str, Any]]] = {}


def get_user_history(user_id: int) -> list[dict[str, Any]]:
    return chat_history_store.get(user_id, [])


def send_chat_message(user_id: int, message: str, mode: str) -> ChatMessageResponse:
    reply = generate_chat_reply(user_message=message, mode=mode)
    emotion_result = analyze_emotion(message)

    user_history = chat_history_store.setdefault(user_id, [])
    user_history.append(
        {
            "role": "user",
            "mode": mode,
            "message": message,
        }
    )
    user_history.append(
        {
            "role": "assistant",
            "message": reply,
        }
    )

    return ChatMessageResponse(
        reply=reply,
        mode=mode,
        emotion=ChatEmotionResult(
            label=emotion_result.label,
            confidence=emotion_result.confidence,
        ),
        history_length=len(user_history),
    )
