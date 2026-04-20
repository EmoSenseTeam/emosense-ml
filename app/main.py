from fastapi import FastAPI

from app.api.v1.api import api_router
import app.core.config  # noqa: F401  # load_dotenv on import
from app.services.behavioral_service import preload_behavioral_model

app = FastAPI(title="EmoSense ML API", version="1.0.0")

try:
    preload_behavioral_model()
except FileNotFoundError:
    pass

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "EmoSense ML service is running"}
