# EmoSense Student — ML API (MVP)

FastAPI-сервис для ML/DL-подсистемы **EmoSense Student**: схемы для четырёх модулей анализа, рабочий baseline для **behavioral**-анализа и каркас для остальных.

## Требования

- Python 3.11+
- Зависимости из `requirements.txt`

## Установка

```bash
cd emosense-ml
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Документация OpenAPI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Endpoints (MVP)

| Метод | Путь | Описание |
|--------|------|----------|
| GET | `/health` | Проверка живости |
| POST | `/api/v1/analysis/behavioral` | Rule-based **emotional_index** |

Остальные модули (conversation, daily, deep): Pydantic-схемы и сервисные заготовки; HTTP-роуты можно добавить по мере готовности моделей.

## Пример: behavioral

**Запрос** `POST /api/v1/analysis/behavioral`

```json
{
  "user_id": "student-42",
  "screen_time_hours": 9.5,
  "sleep_hours": 5.0,
  "physical_activity_steps": 3200,
  "communication_frequency": 2
}
```

**Ответ** (пример)

```json
{
  "emotional_index": 45,
  "risk_level": "moderate",
  "main_behavioral_signals": [
    "low_sleep",
    "high_screen_time",
    "low_physical_activity",
    "low_communication"
  ]
}
```

## Конфигурация

Переменные окружения с префиксом `EMOSENSE_` (см. `app/core/config.py`), например `EMOSENSE_DEBUG=true`.

## Структура

- `app/schemas/` — Pydantic request/response
- `app/services/` — бизнес-логика (baseline в `behavioral_service.py`)
- `app/api/v1/` — роутеры v1
