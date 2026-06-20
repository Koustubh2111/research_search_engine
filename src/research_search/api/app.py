"""
FastAPI Application Factory Module
===================================

This module initializes and configures the FastAPI application for the Research Search Platform.

Key Responsibilities:
    - Create and configure the FastAPI application instance
    - Register API route handlers and routers
    - Manage application lifecycle (startup/shutdown)
    - Set up API versioning and prefixes

Example:
    uvicorn research_search.api.app:app --reload
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager

from research_search.api.routes.health import router as health_router
from research_search.api.routes.ingest import router as ingest_router
from research_search.db.tables import create_tables


# =========================================================
# APPLICATION LIFECYCLE (MODERN FASTAPI WAY)
# =========================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup and shutdown events.

    Startup:
        - Initialize database schema

    Shutdown:
        - Cleanup resources (if needed)
    """

    print("Starting application... creating tables")
    create_tables()

    yield

    print("Shutting down application")


# =========================================================
# FASTAPI APP INSTANCE
# =========================================================
app = FastAPI(
    title="Research Search Platform",
    description="A platform for searching and indexing research papers",
    version="1.0.0",
    lifespan=lifespan
)


# =========================================================
# ROUTES
# =========================================================

# Health check routes: /api/v1/health
app.include_router(health_router, prefix="/api/v1")

# Ingestion routes: /api/v1/ingest/...
app.include_router(ingest_router, prefix="/api/v1")