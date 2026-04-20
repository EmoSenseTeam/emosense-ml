from dotenv import load_dotenv
import os

load_dotenv()

def _get_env_or_default(name: str, default: str) -> str:
    value = os.getenv(name)
    if value is None:
        return default
    normalized = value.strip()
    if not normalized:
        return default
    return normalized


GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY is not None:
    GEMINI_API_KEY = GEMINI_API_KEY.strip() or None
GEMINI_MODEL: str = _get_env_or_default("GEMINI_MODEL", "gemini-1.5-flash")
GEMINI_API_URL: str = _get_env_or_default(
    "GEMINI_API_URL", "https://generativelanguage.googleapis.com/v1beta/models"
)


def get_gemini_api_key() -> str | None:
    return GEMINI_API_KEY


def get_gemini_model() -> str:
    return GEMINI_MODEL


def get_gemini_api_url() -> str:
    return GEMINI_API_URL
