from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

_RU_PATH = Path("data/dictionaries/profanity_ru.txt")
_EN_PATH = Path("data/dictionaries/profanity_en.txt")


def normalize_text(text: str) -> str:
    lowered = text.lower()
    lowered = lowered.replace("*", "").replace("@", "")
    lowered = re.sub(r"[^\w\s]", " ", lowered, flags=re.UNICODE)
    lowered = re.sub(r"\s+", " ", lowered).strip()
    return lowered


@lru_cache(maxsize=1)
def _load_term_sets() -> tuple[set[str], set[str]]:
    single: set[str] = set()
    multi: set[str] = set()
    for path in (_RU_PATH, _EN_PATH):
        if not path.exists():
            raise RuntimeError(f"Profanity dictionary not found: {path}")
        raw = path.read_text(encoding="utf-8", errors="replace")
        for line in raw.splitlines():
            term = line.strip().lower()
            if not term or term.startswith("#"):
                continue
            if " " in term:
                multi.add(re.sub(r"\s+", " ", term).strip())
            else:
                single.add(term)
    return single, multi


def detect_profanity(text: str) -> dict[str, bool | list[str]]:
    normalized = normalize_text(text)
    single_terms, multi_terms = _load_term_sets()

    matched: set[str] = set()
    tokens = re.findall(r"[\w]+", normalized, flags=re.UNICODE)
    for tok in tokens:
        if tok in single_terms:
            matched.add(tok)

    collapsed = re.sub(r"\s+", " ", normalized).strip()
    for phrase in multi_terms:
        if phrase and phrase in collapsed:
            matched.add(phrase)

    matched_list = sorted(matched)
    return {"detected": bool(matched_list), "matched_terms": matched_list}
