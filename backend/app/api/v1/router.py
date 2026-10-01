"""
API v1 Router Aggregator
========================
Combines auth, detection, metrics, and monitoring routers.
"""

from fastapi import APIRouter
from backend.app.api.v1.endpoints import auth, detection, metrics, monitoring

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(detection.router, prefix="/detection", tags=["Threat Detection"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["Metrics & Governance"])
api_router.include_router(monitoring.router, prefix="/monitoring", tags=["Real-time Watcher"])
