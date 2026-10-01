"""
ML Model Inference Service
==========================
Loads the best trained ransomware detection model and scaler for sub-second inference.
"""

import os
import joblib
import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from backend.app.core.config import settings
from ml_pipeline.src.feature_engineering import FeatureEngineer

logger = logging.getLogger(__name__)

class PredictorService:
    """
    Ransomware Prediction Engine wrapper.
    """
    def __init__(self):
        self.model = None
        self.model_name = "RandomForest"
        self.scaler = None
        self.selector = None
        self.feature_names = []
        self._load_artifacts()

    def _load_artifacts(self):
        """Load pickle or joblib model and scaler pipelines."""
        import pickle
        try:
            # Candidate paths for model
            candidate_model_paths = [
                os.path.join(os.path.dirname(__file__), "..", "..", "..", "models", "best_ransomware_model.pkl"),
                os.path.join(os.path.dirname(__file__), "..", "..", "..", "ml_pipeline", "models", "saved_models", "best_ransomware_model.pkl"),
                settings.MODEL_PATH,
            ]
            for path in candidate_model_paths:
                if os.path.exists(path):
                    try:
                        with open(path, "rb") as f:
                            data = pickle.load(f)
                    except Exception:
                        data = joblib.load(path)
                    self.model = data["model"] if isinstance(data, dict) and "model" in data else data
                    self.model_name = data.get("model_name", "RandomForest") if isinstance(data, dict) else "RandomForest"
                    logger.info(f"Loaded trained ML Model [{self.model_name}] from {path}")
                    break
            else:
                logger.warning("Model file not found. Using fallback heuristic predictor.")

            # Candidate paths for scaler
            candidate_scaler_paths = [
                os.path.join(os.path.dirname(__file__), "..", "..", "..", "models", "feature_scaler.pkl"),
                os.path.join(os.path.dirname(__file__), "..", "..", "..", "ml_pipeline", "models", "saved_models", "feature_scaler.pkl"),
                settings.SCALER_PATH,
            ]
            for path in candidate_scaler_paths:
                if os.path.exists(path):
                    try:
                        with open(path, "rb") as f:
                            scaler_data = pickle.load(f)
                    except Exception:
                        scaler_data = joblib.load(path)
                    self.scaler = scaler_data["scaler"]
                    self.selector = scaler_data["selector"]
                    logger.info(f"Loaded fitted Feature Scaler from {path}")
                    break
        except Exception as e:
            logger.error(f"Error loading ML model artifacts: {e}")

    def predict_threat(self, raw_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Run inference over raw feature DataFrame and calculate threat score.
        """
        fe = FeatureEngineer()
        df_domain = fe.create_domain_features(raw_df)
        drop_cols = ["sample_id", "label", "family"]
        feature_cols = [c for c in df_domain.columns if c not in drop_cols]

        X_raw = df_domain[feature_cols].values

        if self.scaler is not None and self.selector is not None:
            X_sel = self.selector.transform(X_raw)
            X_scaled = self.scaler.transform(X_sel)
        else:
            X_scaled = X_raw

        if self.model is not None:
            if hasattr(self.model, "predict_proba"):
                probs = self.model.predict_proba(X_scaled)[0]
                ransomware_prob = float(probs[1])
            elif hasattr(self.model, "decision_function"):
                # Isolation Forest decision_function returns negative value for anomalies (ransomware)
                anomaly_score = float(-self.model.decision_function(X_scaled)[0])
                ransomware_prob = float(1.0 / (1.0 + np.exp(-anomaly_score * 5.0)))
            else:
                raw_pred = self.model.predict(X_scaled)[0]
                # Isolation Forest predict() returns -1 for anomaly, 1 for normal
                if raw_pred == -1:
                    ransomware_prob = 1.0
                elif raw_pred == 1:
                    ransomware_prob = 0.0
                else:
                    ransomware_prob = float(raw_pred)
        else:
            # Fallback heuristic calculation if model binary is building
            entropy = raw_df["entropy"].iloc[0]
            shadow = raw_df["shadow_copies_deleted"].iloc[0]
            if entropy > 7.0 or shadow == 1:
                ransomware_prob = 0.985
            else:
                ransomware_prob = 0.082

        threat_score = round(ransomware_prob * 100.0, 2)
        
        if threat_score >= 75.0:
            risk_level = "CRITICAL"
        elif threat_score >= 40.0:
            risk_level = "SUSPICIOUS"
        else:
            risk_level = "SAFE"

        return {
            "threat_score": threat_score,
            "risk_level": risk_level,
            "prediction_confidence": round(max(ransomware_prob, 1.0 - ransomware_prob) * 100.0, 2),
            "model_used": self.model_name,
            "status": "QUARANTINED" if risk_level == "CRITICAL" else "CLEARED"
        }

predictor_service = PredictorService()
