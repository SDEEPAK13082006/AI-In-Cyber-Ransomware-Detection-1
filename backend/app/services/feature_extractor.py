"""
PE Header & Telemetry Feature Extractor Service
================================================
Extracts 20 static PE features and dynamic telemetry vectors for ML model inference.
"""

import math
import numpy as np
import pandas as pd
from typing import Dict, Any

class FeatureExtractorService:
    """
    Extracts raw static PE parameters and constructs domain-specific features.
    """
    @staticmethod
    def calculate_file_entropy(data: bytes) -> float:
        """Calculate Shannon entropy of byte data (0.0 to 8.0)."""
        if not data:
            return 0.0
        entropy = 0.0
        length = len(data)
        byte_counts = [0] * 256
        for b in data:
            byte_counts[b] += 1
        for count in byte_counts:
            if count > 0:
                p = count / length
                entropy -= p * math.log2(p)
        return round(entropy, 4)

    @staticmethod
    def build_feature_dict(request_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Build raw DataFrame matching the feature layout expected by FeatureEngineer.
        """
        raw_dict = {
            "file_size_kb": float(request_data.get("file_size_kb", 1500.0)),
            "entropy": float(request_data.get("entropy", 4.8)),
            "num_sections": int(request_data.get("num_sections", 4)),
            "has_digital_signature": int(request_data.get("has_digital_signature", 1)),
            "suspicious_imports": int(request_data.get("suspicious_imports", 0)),
            "tls_callbacks_count": int(request_data.get("tls_callbacks_count", 0)),
            "debug_size": int(request_data.get("debug_size", 56)),
            "shadow_copies_deleted": int(request_data.get("shadow_copies_deleted", 0)),
            "registry_run_modified": int(request_data.get("registry_run_modified", 0)),
            "file_rename_rate_per_sec": float(request_data.get("file_rename_rate_per_sec", 0.2)),
            "file_modification_entropy_avg": float(request_data.get("file_modification_entropy_avg", 4.2)),
            "suspicious_extension_changed": int(request_data.get("suspicious_extension_changed", 0)),
            "cpu_spike_ratio": float(request_data.get("cpu_spike_ratio", 0.15)),
            "memory_consumption_mb": float(request_data.get("memory_consumption_mb", 45.0)),
            "network_c2_connections": int(request_data.get("network_c2_connections", 0)),
            "sample_id": "API_REQUEST_001",
            "label": 0,
            "family": "Unknown"
        }
        return pd.DataFrame([raw_dict])
