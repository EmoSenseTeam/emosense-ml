"""Small shared helpers (numeric clamping, etc.)."""

# Функция для ограничения значения в диапазоне
def clamp_int(value: int, low: int = 0, high: int = 100) -> int:
    """Clamp integer to inclusive [low, high]."""
    return max(low, min(high, value))
