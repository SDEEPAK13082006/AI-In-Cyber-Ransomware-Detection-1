"""
Model Training & Experimentation Pipeline
=========================================
Trains multiple ML algorithms (Random Forest, XGBoost, LightGBM, CatBoost, Isolation Forest),
evaluates validation performance, selects the top-performing model, and exports model artifacts.
"""

import os
import json
import joblib
import logging
import numpy as np
import pandas as pd
from typing import Dict, Any

from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
)
from xgboost import XGBClassifier

# Conditional imports for LightGBM and CatBoost
try:
    from lightgbm import LGBMClassifier
    HAS_LGBM = True
except ImportError:
    HAS_LGBM = False

try:
    from catboost import CatBoostClassifier
    HAS_CATBOOST = True
except ImportError:
    HAS_CATBOOST = False

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class ModelTrainer:
    """
    Ransomware Detection Model Trainer comparing Supervised and Anomaly Detection models.
    """
    def __init__(self, processed_data_dir: str, models_output_dir: str):
        self.processed_dir = processed_data_dir
        self.models_dir = models_output_dir
        os.makedirs(self.models_dir, exist_ok=True)

        self.X_train = np.load(os.path.join(self.processed_dir, "X_train.npy"))
        self.y_train = np.load(os.path.join(self.processed_dir, "y_train.npy"))
        self.X_val = np.load(os.path.join(self.processed_dir, "X_val.npy"))
        self.y_val = np.load(os.path.join(self.processed_dir, "y_val.npy"))

    def get_candidate_models(self) -> Dict[str, Any]:
        """
        Define baseline and advanced algorithms with standard hyperparameters.
        """
        models = {
            "RandomForest": RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1),
            "XGBoost": XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, eval_metric="logloss"),
            "IsolationForest": IsolationForest(n_estimators=100, contamination=0.5, random_state=42, n_jobs=-1)
        }

        if HAS_LGBM:
            models["LightGBM"] = LGBMClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, verbose=-1)

        if HAS_CATBOOST:
            models["CatBoost"] = CatBoostClassifier(iterations=150, depth=6, learning_rate=0.1, verbose=0, random_seed=42)

        return models

    def train_and_evaluate_all(self) -> Dict[str, Dict[str, Any]]:
        """
        Train all models and calculate benchmark metrics on the validation dataset.
        """
        candidates = self.get_candidate_models()
        benchmark_results = {}
        best_f1 = -1.0
        best_model_name = ""
        best_model_obj = None

        logger.info(f"Starting Training across {len(candidates)} candidate algorithms...")

        for name, model in candidates.items():
            logger.info(f"Training [{name}]...")
            
            if name == "IsolationForest":
                # Unsupervised Anomaly Detection: fit on benign train samples only
                benign_mask = (self.y_train == 0)
                model.fit(self.X_train[benign_mask])
                
                # Isolation Forest returns 1 for inliers (benign), -1 for outliers (anomaly/ransomware)
                raw_preds = model.predict(self.X_val)
                y_pred = np.where(raw_preds == -1, 1, 0)
                y_probs = -model.decision_function(self.X_val)  # Higher anomaly score = higher risk
            else:
                model.fit(self.X_train, self.y_train)
                y_pred = model.predict(self.X_val)
                y_probs = model.predict_proba(self.X_val)[:, 1]

            acc = float(accuracy_score(self.y_val, y_pred))
            prec = float(precision_score(self.y_val, y_pred, zero_division=0))
            rec = float(recall_score(self.y_val, y_pred, zero_division=0))
            f1 = float(f1_score(self.y_val, y_pred, zero_division=0))
            auc = float(roc_auc_score(self.y_val, y_probs))
            cm = confusion_matrix(self.y_val, y_pred).tolist()

            metrics = {
                "accuracy": round(acc, 4),
                "precision": round(prec, 4),
                "recall": round(rec, 4),
                "f1_score": round(f1, 4),
                "roc_auc": round(auc, 4),
                "confusion_matrix": cm
            }

            benchmark_results[name] = metrics
            logger.info(f"  -> {name} Result | Accuracy: {acc:.4f} | F1-Score: {f1:.4f} | ROC-AUC: {auc:.4f}")

            # Save model checkpoint in .joblib and .pkl formats
            checkpoint_path_joblib = os.path.join(self.models_dir, f"{name.lower()}_model.joblib")
            checkpoint_path_pkl = os.path.join(self.models_dir, f"{name.lower()}_model.pkl")
            root_models_dir = os.path.join(os.path.dirname(__file__), "..", "..", "models")
            os.makedirs(root_models_dir, exist_ok=True)
            root_pkl_path = os.path.join(root_models_dir, f"{name.lower()}_model.pkl")
            
            joblib.dump(model, checkpoint_path_joblib)
            import pickle
            with open(checkpoint_path_pkl, "wb") as f:
                pickle.dump(model, f, protocol=pickle.HIGHEST_PROTOCOL)
            with open(root_pkl_path, "wb") as f:
                pickle.dump(model, f, protocol=pickle.HIGHEST_PROTOCOL)

            if f1 > best_f1:
                best_f1 = f1
                best_model_name = name
                best_model_obj = model

        logger.info(f"[★] Best Model Selected: [{best_model_name}] with F1-Score: {best_f1:.4f}")

        # Save Best Model
        best_model_path_joblib = os.path.join(self.models_dir, "best_ransomware_model.joblib")
        best_model_path_pkl = os.path.join(self.models_dir, "best_ransomware_model.pkl")
        best_root_pkl = os.path.join(root_models_dir, "best_ransomware_model.pkl")
        
        best_payload = {
            "model_name": best_model_name,
            "model": best_model_obj,
            "metrics": benchmark_results[best_model_name]
        }
        joblib.dump(best_payload, best_model_path_joblib)
        with open(best_model_path_pkl, "wb") as f:
            pickle.dump(best_payload, f, protocol=pickle.HIGHEST_PROTOCOL)
        with open(best_root_pkl, "wb") as f:
            pickle.dump(best_payload, f, protocol=pickle.HIGHEST_PROTOCOL)

        # Save benchmark report
        report_path = os.path.join(self.processed_dir, "model_benchmark_results.json")
        with open(report_path, "w") as f:
            json.dump({
                "best_model": best_model_name,
                "benchmark": benchmark_results
            }, f, indent=4)

        logger.info(f"Best model saved to: {best_model_path_joblib} and {best_model_path_pkl}")
        logger.info(f"Benchmark summary saved to: {report_path}")

        return benchmark_results

if __name__ == "__main__":
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
    models_dir = os.path.join(os.path.dirname(__file__), "..", "models", "saved_models")

    trainer = ModelTrainer(processed_data_dir=processed_dir, models_output_dir=models_dir)
    results = trainer.train_and_evaluate_all()
    print("[OK] Model Training & Pipeline Setup completed successfully.")
