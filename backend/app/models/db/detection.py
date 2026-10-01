"""
Detection Record ORM Model
===========================
Stores single file analysis logs, threat scores, risk levels, and SHAP json outputs.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, Text, JSON
from backend.app.core.database import Base

class DetectionRecord(Base):
    __tablename__ = "detection_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String(255), index=True, nullable=False)
    file_hash_sha256 = Column(String(64), index=True, nullable=True)
    file_size_kb = Column(Float, nullable=False)
    entropy = Column(Float, nullable=False)
    threat_score = Column(Float, nullable=False)
    risk_level = Column(String(20), index=True, nullable=False)  # CRITICAL, HIGH, MEDIUM, SAFE
    prediction_confidence = Column(Float, nullable=False)
    shap_explanation = Column(JSON, nullable=True)
    status = Column(String(30), default="QUARANTINED")
    detected_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
