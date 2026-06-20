"""
Health Check Route Module
=========================

This module defines health check endpoints for the Research Search Platform.

Endpoints:
    GET /api/v1/health - Returns the health status of the application

The health endpoint is used by:
    - Load balancers and orchestrators to determine application availability
    - Monitoring systems to verify service uptime
    - Deployment pipelines for readiness probes

This is a critical endpoint for production environments and should remain
lightweight and responsive.
"""

from fastapi import APIRouter

# Create a router instance for organizing health-related endpoints
router = APIRouter()


@router.get("/health")
def health():
    """
    Health Check Endpoint
    
    Returns the current health status of the application.
    
    Returns:
        dict: A dictionary with a "status" key indicating "ok" if the service is healthy
        
    Example:
        GET /api/v1/health
        Response: {"status": "ok"}
    """
    return {"status": "ok"}