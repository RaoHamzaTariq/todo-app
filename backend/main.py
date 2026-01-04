"""
Todo Application Backend
FastAPI server with SQLModel and JWT authentication
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown events."""
    # Startup
    init_db()
    yield
    # Shutdown (future: cleanup connections)


app = FastAPI(
    title="Todo API",
    description="RESTful API for the Todo Application",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Todo API",
        "version": "1.0.0",
        "docs": "/docs",
    }
