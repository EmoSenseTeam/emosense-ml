"""FastAPI application entrypoint — EmoSense Student ML API."""

import logging
from typing import Any

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.v1.behavioral import router as behavioral_router
from app.api.v1.conversation_emotion import router as conversation_router
from app.api.v1.daily import router as daily_router
from app.api.v1.deep import router as deep_router
from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    _request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Return structured 422 body for invalid JSON / field errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch unexpected errors; preserve HTTPException; log and mask others."""
    if isinstance(exc, HTTPException):
        return await http_exception_handler(request, exc)
    logger.exception("Unhandled error: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Liveness probe for orchestrators."""
    return {"status": "ok"}


@app.get("/", tags=["system"])
def root() -> dict[str, Any]:
    """Service metadata."""
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
    }


app.include_router(behavioral_router, prefix=f"{settings.api_v1_prefix}/analysis")
app.include_router(conversation_router, prefix=f"{settings.api_v1_prefix}/analysis")
app.include_router(daily_router, prefix=f"{settings.api_v1_prefix}/analysis")
app.include_router(deep_router, prefix=f"{settings.api_v1_prefix}/analysis")
