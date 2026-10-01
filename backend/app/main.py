"""
Ransomware Defense Platform - FastAPI Backend Main Application
================================================================
Production-grade RESTful API backend serving ML ransomware inference, PE entropy analysis,
real-time filesystem telemetry, SHAP risk explanations, and admin security controls.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.core.database import Base, engine
from backend.app.api.v1.router import api_router
from backend.app.services.predictor import predictor_service

# Configure application logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
)
logger = logging.getLogger("ransomware_defender")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application Lifespan Events.
    Initializes SQL database tables and warms up ML model inference pipelines.
    """
    logger.info("Initializing Ransomware Defense Platform DB tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialized successfully.")
    
    # Warmup ML model predictor
    if predictor_service.model is not None:
        logger.info(f"ML Predictor loaded successfully: [{predictor_service.model_name}]")
    else:
        logger.warning("ML Predictor running in fallback heuristic mode.")

    yield
    
    logger.info("Shutting down Ransomware Defense API engine...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Pre-Encryption Ransomware Defense Platform API for Banking Infrastructure",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_origin_regex=r"https://[a-z0-9-]+\.onrender\.com",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Include API v1 Router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Serve Static Web Interface & Assets
static_dir = os.path.join(os.path.dirname(__file__), "static")
assets_dir = os.path.join(static_dir, "assets")

if os.path.exists(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/health", tags=["Health"])
def health_check():
    """Service health check endpoint."""
    return {
        "status": "HEALTHY",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "active_model": predictor_service.model_name
    }

@app.get("/", include_in_schema=False)
@app.get("/{full_path:path}", include_in_schema=False)
def serve_web_interface(full_path: str = ""):
    """Serve Security Command Center UI dashboard for SPA client routing."""
    # If API or docs route, pass through
    if full_path.startswith("api") or full_path.startswith("docs") or full_path.startswith("redoc") or full_path.startswith("openapi") or full_path == "health":
        return {"message": "Route not found"}
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Ransomware Defense Platform API is running. Visit /api/v1/docs for API specification."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
