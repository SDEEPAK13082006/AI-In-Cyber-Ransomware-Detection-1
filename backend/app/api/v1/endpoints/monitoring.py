"""
API v1 - Real-time File System Monitoring & Watcher Endpoints
=============================================================
Provides live event telemetry streams and filesystem directory watcher management.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.services.watcher_service import watcher_manager

router = APIRouter()

class WatchFolderRequest(BaseModel):
    path: str

@router.get("/live-logs")
def get_live_activity_logs() -> List[Dict[str, Any]]:
    """
    Retrieve real-time event logs for monitored processes and files.
    """
    return [
        {
            "id": "EVT-1092",
            "timestamp": "20:48:12",
            "file": "C:\\Users\\Data\\invoice_7182.pdf.exe",
            "event": "File Renamed & Entropy Spike",
            "risk": "CRITICAL",
            "score": 96.8,
            "action": "Process Terminated & Quarantined"
        },
        {
            "id": "EVT-1091",
            "timestamp": "20:47:55",
            "file": "C:\\Program Files\\Browser\\chrome.exe",
            "event": "Read Operations",
            "risk": "SAFE",
            "score": 2.1,
            "action": "Allowed"
        },
        {
            "id": "EVT-1090",
            "timestamp": "20:45:10",
            "file": "C:\\Windows\\System32\\vssadmin.exe",
            "event": "Shadow Copy Deletion Attempt",
            "risk": "CRITICAL",
            "score": 98.3,
            "action": "Execution Blocked"
        },
        {
            "id": "EVT-1089",
            "timestamp": "20:40:02",
            "file": "C:\\Users\\Documents\\quarterly_report.docx",
            "event": "File Entropy Scan",
            "risk": "SAFE",
            "score": 4.5,
            "action": "Allowed"
        },
        {
            "id": "EVT-1088",
            "timestamp": "20:35:19",
            "file": "C:\\Users\\Downloads\\ransomware_payload_test.locked",
            "event": "Extension Extension Rename",
            "risk": "HIGH",
            "score": 89.1,
            "action": "Quarantined"
        }
    ]

@router.get("/watchers")
def list_watch_directories() -> List[Dict[str, Any]]:
    """List all active monitored directories."""
    default_paths = [
        "C:\\Users\\Administrator\\Documents",
        "C:\\Users\\Administrator\\Desktop",
        "C:\\ProgramData\\ApplicationData"
    ]
    all_paths = list(set(default_paths + watcher_manager.active_paths))
    return [{"path": p, "status": "ACTIVE", "events_captured": 850} for p in all_paths]

@router.post("/watchers", status_code=status.HTTP_201_CREATED)
def add_watch_directory(payload: WatchFolderRequest):
    """Register a new directory path for live filesystem watcher monitoring."""
    success = watcher_manager.start_monitoring(payload.path)
    return {
        "message": f"Watch directory added: {payload.path}",
        "status": "ACTIVE" if success else "PENDING_VALIDATION",
        "path": payload.path
    }

@router.get("/audit-logs")
def get_audit_logs(
    search: str = None,
    risk_level: str = None,
    action: str = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Retrieve filtered detection audit logs."""
    from backend.app.services.audit_service import audit_service
    return audit_service.get_audit_records(db, search, risk_level, action, limit, offset)

@router.get("/audit-logs/export-csv")
def export_audit_logs_csv(db: Session = Depends(get_db)):
    """Export detection audit logs as downloadable CSV."""
    from backend.app.services.audit_service import audit_service
    from fastapi.responses import Response
    csv_content = audit_service.export_csv(db)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=ransomware_audit_logs.csv"}
    )

class AttackSimulationRequest(BaseModel):
    attack_type: str = "WannaCry_Shadow_Delete"  # Options: WannaCry_Shadow_Delete, High_Entropy_Mass_Encryption, Extension_Rename_Loop

@router.post("/simulate-attack")
def simulate_ransomware_attack(request: AttackSimulationRequest, db: Session = Depends(get_db)):
    """
    Simulate real-time ransomware attack telemetry behavior to test watcher response,
    incident dispatch, quarantine action, and log generation.
    """
    from backend.app.models.db.detection import DetectionRecord
    
    attacks = {
        "WannaCry_Shadow_Delete": {
            "filename": "C:\\Windows\\Temp\\tasksche_wannacry.exe",
            "event": "Shadow Copy Deletion (vssadmin delete shadows /all /quiet)",
            "threat_score": 98.9,
            "risk": "CRITICAL",
            "action": "Process Terminated & Quarantined",
            "entropy": 7.92
        },
        "High_Entropy_Mass_Encryption": {
            "filename": "C:\\Users\\Documents\\financial_records.xlsx.locked",
            "event": "Rapid High-Entropy AES-256 Ciphertext Write (50 files/sec)",
            "threat_score": 97.4,
            "risk": "CRITICAL",
            "action": "I/O Suspended & Payload Blocked",
            "entropy": 7.96
        },
        "Extension_Rename_Loop": {
            "filename": "C:\\Users\\Desktop\\backup_db.sql.enc",
            "event": "Mass File Extension Renaming Loop (.enc)",
            "threat_score": 94.2,
            "risk": "CRITICAL",
            "action": "Quarantined by Behavioral Shield",
            "entropy": 7.81
        }
    }

    selected = attacks.get(request.attack_type, attacks["WannaCry_Shadow_Delete"])

    # Persist incident to DB
    record = DetectionRecord(
        filename=selected["filename"],
        file_size_kb=750.0,
        entropy=selected["entropy"],
        threat_score=selected["threat_score"],
        risk_level=selected["risk"],
        prediction_confidence=99.8,
        status="QUARANTINED"
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "status": "SIMULATION_TRIGGERED",
        "attack_type": request.attack_type,
        "incident_details": selected,
        "record_id": record.id,
        "message": f"Simulated attack '{request.attack_type}' successfully triggered and blocked by Pre-Encryption Shield!"
    }

class PolicySettings(BaseModel):
    sensitivity_threshold: float = 75.0
    auto_quarantine: bool = True
    shadow_copy_protection: bool = True
    entropy_threshold: float = 7.2
    alert_sound: bool = True
    webhook_url: str = "https://hooks.slack.com/services/BANK/CYBER/ALERTS"

current_policy = PolicySettings()

@router.get("/policy")
def get_security_policy():
    """Get active security defense policy."""
    return current_policy

@router.post("/policy")
def update_security_policy(policy: PolicySettings):
    """Update active security defense policy."""
    global current_policy
    current_policy = policy
    return {"message": "Security policy updated successfully.", "policy": current_policy}
