from fastapi import APIRouter

from app.api.v1 import behavioral

api_router = APIRouter()
api_router.include_router(
    behavioral.router,
    prefix="/behavioral",
    tags=["Behavioral Analysis"],
)
