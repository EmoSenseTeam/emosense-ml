from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.services.ai_client import analyze_emotion_with_ai, generate_chat_reply


def main() -> None:
    chat_reply = generate_chat_reply("Привет, меня бросила девушка", "soft")
    print("Chat reply:")
    print(chat_reply)
    print()

    emotion_result = analyze_emotion_with_ai("Мне тревожно и тяжело сосредоточиться.")
    print("Emotion result:")
    print(json.dumps(emotion_result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()