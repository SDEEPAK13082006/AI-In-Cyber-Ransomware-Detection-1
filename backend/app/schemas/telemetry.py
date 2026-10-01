"""
Pydantic Schemas for Dashboard Analytics & Watcher Directory Telemetry
"""

from pydantic import BaseModel
from typing import List, Optional

class DashboardSummarySchema(BaseModel):
    totalFilesAnalyzed: int
    suspiciousFiles: int
    ransomwareBlocked: int
    activeWatchers: int
    systemRiskLevel: str
    modelAccuracy: float

class WatcherDirectorySchema(BaseModel):
    folder_path: str
    is_active: bool = True
