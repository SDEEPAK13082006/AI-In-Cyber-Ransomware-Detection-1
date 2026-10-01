"""
Feature Engineering & Preprocessing Pipeline
==============================================
Constructs cybersecurity domain-specific interaction features, applies robust scaling,
and saves fitted scaler artifacts for production inference.
"""

import os
import joblib
import logging
import pandas as pd
import numpy as np
from typing import Tuple
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class FeatureEngineer:
    """
    Feature engineering pipeline for ransomware static and dynamic telemetry data.
    """
    def __init__(self):
        self.scaler = StandardScaler()
        self.variance_selector = VarianceThreshold(threshold=0.01)
        self.feature_names = []

    def create_domain_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create domain-specific cybersecurity interaction features.
        """
        df_engineered = df.copy()

        # 1. Composite Entropy Risk Indicator (High PE entropy + High File Modification entropy)
        df_engineered["composite_entropy_risk"] = (
            df_engineered["entropy"] * df_engineered["file_modification_entropy_avg"]
        )

        # 2. Behavioral Velocity Score (Rename rate * extension changes)
        df_engineered["behavioral_velocity_score"] = (
            df_engineered["file_rename_rate_per_sec"] * (df_engineered["suspicious_extension_changed"] + 1)
        )

        # 3. System Persistence & Sabotage Index
        df_engineered["system_sabotage_index"] = (
            df_engineered["shadow_copies_deleted"] * 3.0 +
            df_engineered["registry_run_modified"] * 2.0 +
            df_engineered["suspicious_imports"] * 0.5
        )

        # 4. Resource Intensity Ratio (CPU spike vs Memory usage)
        df_engineered["resource_intensity_ratio"] = (
            df_engineered["cpu_spike_ratio"] / (df_engineered["memory_consumption_mb"] + 1.0)
        ) * 100.0

        # 5. Network Risk Factor
        df_engineered["network_risk_factor"] = (
            df_engineered["network_c2_connections"] * (1 - df_engineered["has_digital_signature"])
        )

        return df_engineered

    def fit_transform(self, train_df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Fit scaler on training data and return scaled features (X_train, y_train).
        """
        logger.info("Engineering features for Training Set...")
        df_engineered = self.create_domain_features(train_df)

        drop_cols = ["sample_id", "label", "family"]
        feature_cols = [c for c in df_engineered.columns if c not in drop_cols]
        self.feature_names = feature_cols

        X_raw = df_engineered[feature_cols].values
        y_train = df_engineered["label"].values

        # Variance thresholding
        X_selected = self.variance_selector.fit_transform(X_raw)
        
        # Standard scaling
        X_scaled = self.scaler.fit_transform(X_selected)

        logger.info(f"Engineered {X_scaled.shape[1]} features for training.")
        return X_scaled, y_train

    def transform(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Transform validation or test set using fitted parameters.
        """
        df_engineered = self.create_domain_features(df)
        drop_cols = ["sample_id", "label", "family"]
        feature_cols = [c for c in df_engineered.columns if c not in drop_cols]

        X_raw = df_engineered[feature_cols].values
        y = df_engineered["label"].values

        X_selected = self.variance_selector.transform(X_raw)
        X_scaled = self.scaler.transform(X_selected)
        return X_scaled, y

    def save_pipeline(self, output_dir: str):
        """
        Save feature scaler and feature metadata to joblib & pickle for serving API inference.
        """
        import pickle
        import json

        os.makedirs(output_dir, exist_ok=True)
        scaler_payload = {"scaler": self.scaler, "selector": self.variance_selector}

        # Paths
        scaler_joblib = os.path.join(output_dir, "feature_scaler.joblib")
        meta_path = os.path.join(output_dir, "feature_names.json")
        root_models_dir = os.path.join(os.path.dirname(__file__), "..", "..", "models")
        os.makedirs(root_models_dir, exist_ok=True)

        joblib.dump(scaler_payload, scaler_joblib)
        with open(meta_path, "w") as f:
            json.dump(self.feature_names, f, indent=4)

        # Sync to root models directory
        root_scaler_pkl = os.path.join(root_models_dir, "feature_scaler.pkl")
        root_meta_json = os.path.join(root_models_dir, "feature_names.json")
        with open(root_scaler_pkl, "wb") as f:
            pickle.dump(scaler_payload, f, protocol=pickle.HIGHEST_PROTOCOL)
        with open(root_meta_json, "w") as f:
            json.dump(self.feature_names, f, indent=4)

        logger.info(f"Feature scaler saved to: {scaler_joblib} and {root_scaler_pkl}")
        logger.info(f"Feature metadata saved to: {meta_path} and {root_meta_json}")

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
    from ml_pipeline.src.data_loader import RansomwareDataLoader

    raw_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "ransomware_dataset.csv")
    loader = RansomwareDataLoader(data_path=raw_path)
    train_df, val_df, test_df = loader.get_stratified_splits()

    fe = FeatureEngineer()
    X_train, y_train = fe.fit_transform(train_df)
    X_val, y_val = fe.transform(val_df)
    X_test, y_test = fe.transform(test_df)

    processed_dir = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
    fe.save_pipeline(output_dir=processed_dir)

    # Save arrays for ML training phase
    np.save(os.path.join(processed_dir, "X_train.npy"), X_train)
    np.save(os.path.join(processed_dir, "y_train.npy"), y_train)
    np.save(os.path.join(processed_dir, "X_val.npy"), X_val)
    np.save(os.path.join(processed_dir, "y_val.npy"), y_val)
    np.save(os.path.join(processed_dir, "X_test.npy"), X_test)
    np.save(os.path.join(processed_dir, "y_test.npy"), y_test)

    print("[OK] Feature Engineering phase completed successfully.")
