"""
FastAPI Application Factory Module
===================================

This module initializes and configures the FastAPI application for the Research Search Platform.

Key Responsibilities:
    - Create and configure the FastAPI application instance
    - Register API route handlers and routers
    - Set up API versioning and prefixes

The application follows a modular architecture where core routes are organized
in the routes/ directory and included here for centralized app setup.

Example:
    The app is typically run using:
    >>> uvicorn research_search.api.app:app --reload
"""

from fastapi import FastAPI
from research_search.api.routes.health import router as health_router

# Initialize the FastAPI application with metadata
# This creates the core ASGI application instance with swagger documentation
app = FastAPI(
    title="Research Search Platform",
    description="A platform for searching and indexing research papers",
    version="1.0.0"
)

# Include the health check route with API v1 prefix
# Health routes: GET /api/v1/health
app.include_router(health_router, prefix="/api/v1")