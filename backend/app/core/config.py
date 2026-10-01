"""
Backend Core Configuration Settings
====================================
Uses Pydantic BaseSettings to read environment variables.
"""

import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Ransomware Detection Platform API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = "defender_ransomware_detection_jwt_secret_key_2026_production_grade"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Database Settings
    DATABASE_URL: str = "sqlite:///./ransomware_defender.db"
    
    # ML Engine Settings (.pkl models)
    MODEL_PATH: str = os.path.join(os.path.dirname(__file__), "..", "..", "..", "models", "best_ransomware_model.pkl")
    SCALER_PATH: str = os.path.join(os.path.dirname(__file__), "..", "..", "..", "models", "feature_scaler.pkl")
    FEATURE_NAMES_PATH: str = os.path.join(os.path.dirname(__file__), "..", "..", "..", "models", "feature_names.json")

    # Threat Risk Threshold (0-100)
    RANSOMWARE_THRESHOLD: float = 75.0

    # CORS Origins
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:3000"]

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
