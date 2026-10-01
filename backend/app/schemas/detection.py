"""
Pydantic Schemas for File Threat Analysis & SHAP Explanations
"""

from pydantic import BaseModel
from typing import List, Optional, Any

class SingleFileAnalysisRequest(BaseModel):
    filename: str
    file_size_kb: float
    entropy: float
    num_sections: Optional[int] = 4
    has_digital_signature: Optional[int] = 0
    suspicious_imports: Optional[int] = 2
    shadow_copies_deleted: Optional[int] = 0
    registry_run_modified: Optional[int] = 0
    file_rename_rate_per_sec: Optional[float] = 0.5
    file_modification_entropy_avg: Optional[float] = 4.2
    suspicious_extension_changed: Optional[int] = 0
    cpu_spike_ratio: Optional[float] = 0.15
    memory_consumption_mb: Optional[float] = 45.0
    network_c2_connections: Optional[int] = 0

class SHAPDriverSchema(BaseModel):
    feature: str
    shap_value: float
    scaled_value: float
    impact: str

class DetectionResponseSchema(BaseModel):
    filename: str
    threat_score: float
    risk_level: str
    prediction_confidence: float
    top_risk_drivers: List[SHAPDriverSchema]
    status: str
