from fastapi import APIRouter

from app.api.v1 import behavioral, chat, emotion, moderation

api_router = APIRouter()
api_router.include_router(
    behavioral.router,
    prefix="/behavioral",
    tags=["Behavioral Analysis"],
)
api_router.include_router(
    chat.router,
    prefix="/chat",
    tags=["AI Chat"],
)
api_router.include_router(
    emotion.router,
    prefix="/emotion",
    tags=["Emotion Analysis"],
)
api_router.include_router(
    moderation.router,
    prefix="/moderation",
    tags=["Moderation"],
)
