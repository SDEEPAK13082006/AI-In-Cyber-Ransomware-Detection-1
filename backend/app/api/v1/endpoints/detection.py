"""
API v1 - Ransomware Threat Detection Endpoints
==============================================
Provides single-file static/dynamic telemetry analysis and batch directory scanning.
Integrates ML Predictor Engine, SHAP Feature Explainer, and Multi-channel Alerting.
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.schemas.detection import SingleFileAnalysisRequest, DetectionResponseSchema
from backend.app.services.feature_extractor import FeatureExtractorService
from backend.app.services.predictor import predictor_service
from backend.app.services.shap_service import shap_service
from backend.app.services.alert_service import alert_service
from backend.app.models.db.detection import DetectionRecord

router = APIRouter()

@router.post("/analyze", response_model=DetectionResponseSchema)
def analyze_single_file(request: SingleFileAnalysisRequest, db: Session = Depends(get_db)):
    """
    Analyze single PE binary file or system process telemetry for ransomware indicators.
    Run ML inference, extract SHAP driver impacts, trigger alerts if risk exceeds threshold,
    and persist detection audit record to SQLite database.
    """
    try:
        # Convert request pydantic model to feature dataframe layout
        raw_df = FeatureExtractorService.build_feature_dict(request.model_dump())
        
        # 1. Run ML Prediction Engine
        prediction_res = predictor_service.predict_threat(raw_df)
        threat_score = prediction_res["threat_score"]
        risk_level = prediction_res["risk_level"]
        prediction_confidence = prediction_res["prediction_confidence"]
        status_code = prediction_res["status"]

        # 2. Extract SHAP Risk Drivers
        top_drivers = shap_service.get_explanation_for_request(raw_df)

        # 3. Dispatch Alerts if threat score >= threshold
        alert_service.dispatch_alert(request.filename, threat_score, risk_level)

        # 4. Save Detection Record to Database
        db_record = DetectionRecord(
            filename=request.filename,
            file_size_kb=request.file_size_kb,
            entropy=request.entropy,
            threat_score=threat_score,
            risk_level=risk_level,
            prediction_confidence=prediction_confidence,
            shap_explanation=top_drivers,
            status=status_code
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)

        return {
            "filename": request.filename,
            "threat_score": threat_score,
            "risk_level": risk_level,
            "prediction_confidence": prediction_confidence,
            "top_risk_drivers": top_drivers,
            "status": status_code
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing ransomware analysis pipeline: {str(e)}"
        )

@router.post("/batch", response_model=List[DetectionResponseSchema])
def analyze_batch_files(requests: List[SingleFileAnalysisRequest], db: Session = Depends(get_db)):
    """
    Analyze multiple file samples in batch for directory audit operations.
    """
    results = []
    for req in requests:
        res = analyze_single_file(req, db)
        results.append(res)
    return results

@router.get("/sample-payloads")
def get_sample_payloads():
    """
    Retrieve pre-configured sample binaries and malware profiles for 1-click test analysis.
    """
    return [
        {
            "id": "sample-wannacry",
            "name": "WannaCry.v2.exe (EternalBlue Ransomware)",
            "type": "RANSOMWARE",
            "payload": {
                "filename": "WannaCry_MS17_010.exe",
                "file_size_kb": 3514.0,
                "entropy": 7.89,
                "num_sections": 6,
                "has_digital_signature": 0,
                "suspicious_imports": 8,
                "tls_callbacks_count": 1,
                "debug_size": 0,
                "shadow_copies_deleted": 1,
                "registry_run_modified": 1,
                "file_rename_rate_per_sec": 48.5,
                "file_modification_entropy_avg": 7.82,
                "suspicious_extension_changed": 25,
                "cpu_spike_ratio": 0.88,
                "memory_consumption_mb": 42.0,
                "network_c2_connections": 3
            }
        },
        {
            "id": "sample-lockbit",
            "name": "LockBit_3.0_Black.exe (High Velocity)",
            "type": "RANSOMWARE",
            "payload": {
                "filename": "LockBit3_Payload_Sample.bin",
                "file_size_kb": 890.0,
                "entropy": 7.95,
                "num_sections": 7,
                "has_digital_signature": 0,
                "suspicious_imports": 12,
                "tls_callbacks_count": 2,
                "debug_size": 28,
                "shadow_copies_deleted": 1,
                "registry_run_modified": 1,
                "file_rename_rate_per_sec": 65.0,
                "file_modification_entropy_avg": 7.91,
                "suspicious_extension_changed": 40,
                "cpu_spike_ratio": 0.94,
                "memory_consumption_mb": 55.0,
                "network_c2_connections": 4
            }
        },
        {
            "id": "sample-ryuk",
            "name": "Ryuk_Banking_Trojan_Dropped.exe",
            "type": "RANSOMWARE",
            "payload": {
                "filename": "Ryuk_Encrypted_Drops.exe",
                "file_size_kb": 1200.0,
                "entropy": 7.74,
                "num_sections": 5,
                "has_digital_signature": 0,
                "suspicious_imports": 7,
                "tls_callbacks_count": 0,
                "debug_size": 0,
                "shadow_copies_deleted": 1,
                "registry_run_modified": 1,
                "file_rename_rate_per_sec": 38.0,
                "file_modification_entropy_avg": 7.65,
                "suspicious_extension_changed": 18,
                "cpu_spike_ratio": 0.79,
                "memory_consumption_mb": 35.0,
                "network_c2_connections": 2
            }
        },
        {
            "id": "sample-excel",
            "name": "Q3_Financial_Statement.xlsx (Benign Office)",
            "type": "BENIGN",
            "payload": {
                "filename": "Q3_Financial_Statement.xlsx",
                "file_size_kb": 1540.0,
                "entropy": 4.35,
                "num_sections": 4,
                "has_digital_signature": 1,
                "suspicious_imports": 0,
                "tls_callbacks_count": 0,
                "debug_size": 56,
                "shadow_copies_deleted": 0,
                "registry_run_modified": 0,
                "file_rename_rate_per_sec": 0.0,
                "file_modification_entropy_avg": 4.10,
                "suspicious_extension_changed": 0,
                "cpu_spike_ratio": 0.12,
                "memory_consumption_mb": 115.0,
                "network_c2_connections": 0
            }
        },
        {
            "id": "sample-chrome",
            "name": "Chrome_Browser_Setup.exe (Benign Signed)",
            "type": "BENIGN",
            "payload": {
                "filename": "Chrome_Browser_Setup.exe",
                "file_size_kb": 2400.0,
                "entropy": 5.82,
                "num_sections": 5,
                "has_digital_signature": 1,
                "suspicious_imports": 1,
                "tls_callbacks_count": 0,
                "debug_size": 84,
                "shadow_copies_deleted": 0,
                "registry_run_modified": 0,
                "file_rename_rate_per_sec": 0.05,
                "file_modification_entropy_avg": 4.45,
                "suspicious_extension_changed": 0,
                "cpu_spike_ratio": 0.18,
                "memory_consumption_mb": 140.0,
                "network_c2_connections": 1
            }
        }
    ]
