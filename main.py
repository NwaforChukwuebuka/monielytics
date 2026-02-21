"""FastAPI application entrypoint."""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.analytics import router as analytics_router
from app.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ensure tables exist on startup."""
    init_db()
    yield


app = FastAPI(
    title="Moniepoint Analytics API",
    description="Merchant activity analytics for the Moniepoint ecosystem.",
    lifespan=lifespan,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)


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
