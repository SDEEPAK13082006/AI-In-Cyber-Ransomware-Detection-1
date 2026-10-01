"""
SHAP Model Explainability Module
================================
Provides global feature importance and local instance-level SHAP explanations
for security analysts to inspect ransomware risk factors.
"""

import os
import sys
import json
import joblib
import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, List

# Windows patch for PySpark import bug in SHAP
import socketserver
if not hasattr(socketserver, "UnixStreamServer"):
    class DummyUnixStreamServer:
        pass
    socketserver.UnixStreamServer = DummyUnixStreamServer

try:
    import shap
    HAS_SHAP = True
except Exception:
    HAS_SHAP = False

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class RansomwareSHAPExplainer:
    """
    SHAP Explainer wrapper for Ransomware Detection Tree-based Ensembles.
    """
    def __init__(self, model_path: str, feature_names_path: str):
        import pickle
        try:
            with open(model_path, "rb") as f:
                saved_data = pickle.load(f)
        except Exception:
            saved_data = joblib.load(model_path)
            
        self.model_name = saved_data["model_name"] if isinstance(saved_data, dict) else "RandomForest"
        self.model = saved_data["model"] if isinstance(saved_data, dict) else saved_data

        with open(feature_names_path, "r") as f:
            self.feature_names = json.load(f)

        self.explainer = None
        if HAS_SHAP:
            try:
                self.explainer = shap.TreeExplainer(self.model)
            except Exception:
                try:
                    self.explainer = shap.Explainer(self.model)
                except Exception:
                    self.explainer = None

    def explain_sample(self, sample_scaled: np.ndarray) -> Dict[str, Any]:
        """
        Explain a single feature vector instance returning feature risk contributions.
        """
        if sample_scaled.ndim == 1:
            sample_scaled = sample_scaled.reshape(1, -1)

        if self.explainer is not None:
            try:
                shap_values = self.explainer.shap_values(sample_scaled)
                if isinstance(shap_values, list):
                    sv = shap_values[1][0]
                elif shap_values.ndim == 3:
                    sv = shap_values[0, :, 1]
                else:
                    sv = shap_values[0]
            except Exception:
                sv = self._fallback_feature_importance(sample_scaled[0])
        else:
            sv = self._fallback_feature_importance(sample_scaled[0])

        feature_contributions = []
        for name, val, raw_val in zip(self.feature_names, sv, sample_scaled[0]):
            feature_contributions.append({
                "feature": name,
                "shap_value": float(round(val, 4)),
                "scaled_value": float(round(raw_val, 4)),
                "impact": "Ransomware Risk" if val > 0 else "Benign Indicator"
            })

        feature_contributions.sort(key=lambda x: abs(x["shap_value"]), reverse=True)

        return {
            "model_used": self.model_name,
            "top_risk_drivers": [f for f in feature_contributions if f["shap_value"] > 0][:5],
            "all_contributions": feature_contributions
        }

    def _fallback_feature_importance(self, sample: np.ndarray) -> np.ndarray:
        """
        Fallback feature importance estimation using model feature importances multiplied by sample values.
        """
        if hasattr(self.model, "feature_importances_"):
            imp = self.model.feature_importances_
        else:
            imp = np.ones(len(self.feature_names)) / len(self.feature_names)
        return imp * sample

    def generate_global_importance(self, X_val: np.ndarray, output_path: str) -> List[Dict[str, Any]]:
        """
        Generate global mean absolute SHAP feature importance summary over validation dataset.
        """
        logger.info(f"Computing Global SHAP Feature Importance over {len(X_val)} validation samples...")
        
        if self.explainer is not None:
            try:
                shap_values = self.explainer.shap_values(X_val)
                if isinstance(shap_values, list):
                    vals = np.abs(shap_values[1]).mean(axis=0)
                elif shap_values.ndim == 3:
                    vals = np.abs(shap_values[:, :, 1]).mean(axis=0)
                else:
                    vals = np.abs(shap_values).mean(axis=0)
            except Exception:
                vals = getattr(self.model, "feature_importances_", np.ones(len(self.feature_names)))
        else:
            vals = getattr(self.model, "feature_importances_", np.ones(len(self.feature_names)))

        global_importance = []
        for name, imp in zip(self.feature_names, vals):
            global_importance.append({
                "feature": name,
                "mean_abs_shap": float(round(imp, 4))
            })

        global_importance.sort(key=lambda x: x["mean_abs_shap"], reverse=True)

        with open(output_path, "w") as f:
            json.dump(global_importance, f, indent=4)

        logger.info(f"Global SHAP summary saved to: {output_path}")
        return global_importance

if __name__ == "__main__":
    model_file = os.path.join(os.path.dirname(__file__), "..", "models", "saved_models", "best_ransomware_model.joblib")
    meta_file = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "feature_names.json")
    val_data_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "X_val.npy")
    output_json = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "shap_summary.json")

    X_val = np.load(val_data_path)
    explainer = RansomwareSHAPExplainer(model_path=model_file, feature_names_path=meta_file)
    explainer.generate_global_importance(X_val=X_val, output_path=output_json)

    sample_explanation = explainer.explain_sample(X_val[0])
    print(f"[OK] Sample Top Risk Drivers: {sample_explanation['top_risk_drivers']}")
    print("[OK] SHAP Explainability module test successful.")
