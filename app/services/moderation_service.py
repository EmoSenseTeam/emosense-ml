from __future__ import annotations

from typing import Any

from app.services.moderation_model import predict_signals
from app.services.profanity_service import detect_profanity


def moderate_text(user_id: int, text: str) -> dict[str, Any]:
    normalized = text.strip()
    if not normalized:
        raise ValueError("text must not be empty")

    toxicity = predict_signals(normalized)
    profanity = detect_profanity(normalized)

    sexual: dict[str, bool | float] = {"detected": False, "confidence": 0.0}
    extremism: dict[str, bool | float] = {"detected": False, "confidence": 0.0}
    sexism: dict[str, bool | float] = {"detected": False, "confidence": 0.0}

    threat = float(toxicity.get("threat", 0.0))
    identity_hate = float(toxicity.get("identity_hate", 0.0))
    toxic = float(toxicity.get("toxic", 0.0))
    insult = float(toxicity.get("insult", 0.0))

    profanity_detected = bool(profanity.get("detected"))
    extremism_detected = bool(extremism.get("detected"))
    sexual_detected = bool(sexual.get("detected"))

    if extremism_detected:
        final_label = "extremism"
    elif sexual_detected:
        final_label = "sexual_18_plus"
    elif threat >= 0.5 or identity_hate >= 0.5:
        final_label = "aggressive"
    elif profanity_detected:
        final_label = "profanity"
    elif toxic >= 0.5 or insult >= 0.5:
        final_label = "toxic"
    else:
        final_label = "safe"

    if final_label == "safe":
        action = "allow"
    elif final_label in ("toxic", "profanity"):
        action = "flag"
    elif final_label in ("aggressive", "sexual_18_plus", "extremism"):
        action = "block"
    else:
        action = "allow"

    max_toxicity = max(float(v) for v in toxicity.values()) if toxicity else 0.0
    if profanity_detected:
        confidence = max(max_toxicity, 0.99)
    else:
        confidence = max_toxicity

    reason_by_label: dict[str, str] = {
        "safe": "Content is safe",
        "toxic": "Toxic or insulting language detected",
        "profanity": "Profanity detected",
        "aggressive": "Aggressive or threatening language detected",
        "sexual_18_plus": "Adult sexual content detected",
        "extremism": "Extremist content detected",
    }
    reason = reason_by_label.get(final_label, "Content is safe")

    signals: dict[str, Any] = {
        "toxicity": toxicity,
        "profanity": profanity,
        "sexual": sexual,
        "extremism": extremism,
        "sexism": sexism,
    }

    return {
        "user_id": user_id,
        "final_label": final_label,
        "action": action,
        "confidence": float(confidence),
        "signals": signals,
        "reason": reason,
    }
