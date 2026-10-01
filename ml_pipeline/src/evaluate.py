"""
Model Evaluation & Testing Module
=================================
Evaluates trained models on the holdout test set, performs 5-Fold Stratified Cross-Validation,
generates confusion matrices, and exports comprehensive metric artifacts.
"""

import os
import json
import joblib
import logging
import numpy as np
import pandas as pd
from typing import Dict, Any

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, classification_report
)
from sklearn.model_selection import StratifiedKFold, cross_val_score

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class ModelEvaluator:
    """
    Ransomware Detection Model Evaluator for test set metrics and cross-validation.
    """
    def __init__(self, processed_data_dir: str, model_path: str):
        self.processed_dir = processed_data_dir
        self.model_path = model_path

        self.X_test = np.load(os.path.join(self.processed_dir, "X_test.npy"))
        self.y_test = np.load(os.path.join(self.processed_dir, "y_test.npy"))
        
        self.X_train = np.load(os.path.join(self.processed_dir, "X_train.npy"))
        self.y_train = np.load(os.path.join(self.processed_dir, "y_train.npy"))

        import pickle
        try:
            with open(self.model_path, "rb") as f:
                saved_data = pickle.load(f)
        except Exception:
            saved_data = joblib.load(self.model_path)

        self.model_name = saved_data["model_name"] if isinstance(saved_data, dict) else "RandomForest"
        self.model = saved_data["model"] if isinstance(saved_data, dict) else saved_data

    def evaluate_test_set(self) -> Dict[str, Any]:
        """
        Evaluate best model performance on unseen test data.
        """
        logger.info(f"Evaluating Best Model [{self.model_name}] on Holdout Test Set ({len(self.X_test)} samples)...")

        y_pred = self.model.predict(self.X_test)
        if hasattr(self.model, "predict_proba"):
            y_probs = self.model.predict_proba(self.X_test)[:, 1]
        else:
            y_probs = y_pred

        acc = float(accuracy_score(self.y_test, y_pred))
        prec = float(precision_score(self.y_test, y_pred, zero_division=0))
        rec = float(recall_score(self.y_test, y_pred, zero_division=0))
        f1 = float(f1_score(self.y_test, y_pred, zero_division=0))
        auc = float(roc_auc_score(self.y_test, y_probs))
        cm = confusion_matrix(self.y_test, y_pred).tolist()
        clr = classification_report(self.y_test, y_pred, output_dict=True)

        # 5-Fold Stratified Cross-Validation
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        cv_scores = cross_val_score(self.model, self.X_train, self.y_train, cv=cv, scoring="f1")
        cv_mean = float(cv_scores.mean())
        cv_std = float(cv_scores.std())

        metrics = {
            "model_name": self.model_name,
            "test_accuracy": round(acc, 4),
            "test_precision": round(prec, 4),
            "test_recall": round(rec, 4),
            "test_f1_score": round(f1, 4),
            "test_roc_auc": round(auc, 4),
            "cv_f1_mean": round(cv_mean, 4),
            "cv_f1_std": round(cv_std, 4),
            "confusion_matrix": cm,
            "classification_report": clr
        }

        output_path = os.path.join(self.processed_dir, "evaluation_report.json")
        with open(output_path, "w") as f:
            json.dump(metrics, f, indent=4)

        logger.info(f"Test Accuracy  : {acc:.4f}")
        logger.info(f"Test Precision : {prec:.4f}")
        logger.info(f"Test Recall    : {rec:.4f}")
        logger.info(f"Test F1-Score  : {f1:.4f}")
        logger.info(f"Test ROC-AUC   : {auc:.4f}")
        logger.info(f"5-Fold CV F1   : {cv_mean:.4f} (+/- {cv_std:.4f})")
        logger.info(f"Evaluation report written to: {output_path}")

        return metrics

if __name__ == "__main__":
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
    model_file = os.path.join(os.path.dirname(__file__), "..", "models", "saved_models", "best_ransomware_model.joblib")

    evaluator = ModelEvaluator(processed_data_dir=processed_dir, model_path=model_file)
    evaluator.evaluate_test_set()
    print("[OK] Model Evaluation completed successfully.")
