"""Conversational emotion analysis — stub for future ML models."""

from app.schemas.conversation import ConversationEmotionRequest, ConversationEmotionResponse


def analyze_conversation(_payload: ConversationEmotionRequest) -> ConversationEmotionResponse:
    """
    Placeholder: wire tokenizer + classifier here.

    Not implemented in MVP; returns a neutral stub for API wiring tests.
    """
    return ConversationEmotionResponse(
        emotion_label="neutral",
        stress_probability=0.0,
        extracted_triggers=[],
        confidence_score=0.0,
    )
