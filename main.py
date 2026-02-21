"""FastAPI application entrypoint."""
import logging
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.analytics import router as analytics_router
from app.db import init_db

LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

logger = logging.getLogger("monielytics")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)


class RequestLogMiddleware(BaseHTTPMiddleware):
    """Log each request and response with status and duration."""

    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "%s %s %s %.2fms",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ensure tables exist on startup."""
    logger.info("Starting up: initializing database schema")
    init_db()
    logger.info("Application ready")
    yield
    logger.info("Shutting down")


app = FastAPI(
    title="Moniepoint Analytics API",
    description="Merchant activity analytics for the Moniepoint.",
    lifespan=lifespan,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)
app.add_middleware(RequestLogMiddleware)


@app.get("/")
def root():
    """Root endpoint with API info and links."""
    return {
        "message": "Moniepoint Analytics API",
        "docs": "/api/docs",
        "analytics": "/analytics/top-merchant",
        "openapi": "/api/openapi.json",
    }


app.include_router(analytics_router)
