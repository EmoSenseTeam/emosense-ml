from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
import time
from typing import Any

import requests

from app.core.config import get_gemini_api_key, get_gemini_api_url, get_gemini_model

_PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"
_REQUEST_TIMEOUT_SECONDS = 30
_MAX_RETRIES = 3
_RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
_BASE_RETRY_DELAY_SECONDS = 1.0


@lru_cache(maxsize=8)
def read_prompt_file(file_name: str) -> str:
    path = _PROMPTS_DIR / file_name
    if not path.exists():
        raise RuntimeError(f"Prompt file not found: {path}")
    content = path.read_text(encoding="utf-8").strip()
    if not content:
        raise RuntimeError(f"Prompt file is empty: {path}")
    return content


def extract_text_from_gemini_response(data: dict[str, Any]) -> str:
    try:
        return str(data["candidates"][0]["content"]["parts"][0]["text"]).strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"Unexpected Gemini response format: {data}") from exc


def _build_gemini_endpoint() -> str:
    api_key = get_gemini_api_key()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured. Please set it in .env")
    base_url = get_gemini_api_url().rstrip("/")
    if not base_url.endswith("/models"):
        base_url = f"{base_url}/models"

    model = get_gemini_model().strip()
    if model.startswith("models/"):
        model = model[len("models/") :]
    if not model:
        raise RuntimeError(
            "GEMINI_MODEL is empty. Please set a valid model name in .env"
        )
    return f"{base_url}/{model}:generateContent?key={api_key}"


def _post_to_gemini(system_instruction: str, user_text: str) -> str:
    url = _build_gemini_endpoint()
    payload = {
        "system_instruction": {
            "parts": [{"text": system_instruction}],
        },
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_text}],
            }
        ],
    }

    response: requests.Response | None = None
    last_request_error: requests.RequestException | None = None
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            response = requests.post(
                url,
                json=payload,
                timeout=_REQUEST_TIMEOUT_SECONDS,
            )
            last_request_error = None
        except requests.RequestException as exc:
            last_request_error = exc
            if attempt == _MAX_RETRIES:
                raise RuntimeError(
                    f"Failed to call Gemini API after {attempt} attempts: {exc}"
                ) from exc
            time.sleep(_BASE_RETRY_DELAY_SECONDS * (2 ** (attempt - 1)))
            continue

        if response.status_code in _RETRYABLE_STATUS_CODES and attempt < _MAX_RETRIES:
            time.sleep(_BASE_RETRY_DELAY_SECONDS * (2 ** (attempt - 1)))
            continue

        if response.status_code >= 400:
            raise RuntimeError(
                f"Gemini API error {response.status_code} after {attempt} attempts: {response.text}"
            )

        break

    if response is None:
        if last_request_error is not None:
            raise RuntimeError(
                f"Failed to call Gemini API: {last_request_error}"
            ) from last_request_error
        raise RuntimeError("Gemini API request failed without a response.")

    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError(
            f"Gemini API returned non-JSON response: {response.text}"
        ) from exc
    return extract_text_from_gemini_response(data)


def generate_chat_reply(user_message: str, mode: str) -> str:
    if mode == "soft":
        prompt_file = "soft_prompt.txt"
    elif mode == "strict":
        prompt_file = "strict_prompt.txt"
    else:
        raise ValueError("mode must be either 'soft' or 'strict'")

    instruction = read_prompt_file(prompt_file)
    return _post_to_gemini(instruction, user_message)


def _extract_json_payload(raw_text: str) -> str:
    text = raw_text.strip()
    if text.startswith("```"):
        lines = [line for line in text.splitlines() if not line.strip().startswith("```")]
        text = "\n".join(lines).strip()

    start_index = text.find("{")
    end_index = text.rfind("}")
    if start_index == -1 or end_index == -1 or end_index < start_index:
        raise RuntimeError(
            f"Emotion analysis response is not valid JSON: {raw_text}"
        )
    return text[start_index : end_index + 1]


def analyze_emotion_with_ai(text: str) -> dict[str, Any]:
    instruction = read_prompt_file("emotion_prompt.txt")
    raw_response = _post_to_gemini(instruction, text)
    json_payload = _extract_json_payload(raw_response)
    try:
        parsed = json.loads(json_payload)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Emotion analysis response is not valid JSON: {raw_response}"
        ) from exc

    if not isinstance(parsed, dict):
        raise RuntimeError(
            f"Emotion analysis response must be a JSON object: {raw_response}"
        )
    return parsed
