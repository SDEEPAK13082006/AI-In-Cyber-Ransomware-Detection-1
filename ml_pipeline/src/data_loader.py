"""
Data Loader & Dataset Ingestion Utility
=======================================
Handles raw dataset ingestion, validation checks, missing value handling,
and train/validation/test splits with stratification.
"""

import os
import logging
import pandas as pd
from typing import Tuple, Dict, Any
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class RansomwareDataLoader:
    """
    DataLoader class for loading and preprocessing raw telemetry and static feature datasets.
    """
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df: pd.DataFrame = None

    def load_raw_data(self) -> pd.DataFrame:
        """
        Load CSV data from disk and perform basic integrity checks.
        """
        if not os.path.exists(self.data_path):
            logger.error(f"Data file not found at: {self.data_path}")
            raise FileNotFoundError(f"File not found: {self.data_path}")

        logger.info(f"Loading raw dataset from: {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        logger.info(f"Loaded {len(self.df)} records with {len(self.df.columns)} features.")
        return self.df

    def validate_schema(self) -> bool:
        """
        Validate dataset schema and check for missing/null values.
        """
        if self.df is None:
            self.load_raw_data()

        required_columns = [
            "file_size_kb", "entropy", "num_sections", "has_digital_signature",
            "suspicious_imports", "tls_callbacks_count", "debug_size",
            "shadow_copies_deleted", "registry_run_modified", "file_rename_rate_per_sec",
            "file_modification_entropy_avg", "suspicious_extension_changed",
            "cpu_spike_ratio", "memory_consumption_mb", "network_c2_connections", "label"
        ]

        missing_cols = [col for col in required_columns if col not in self.df.columns]
        if missing_cols:
            logger.error(f"Missing required columns in dataset: {missing_cols}")
            raise ValueError(f"Missing columns: {missing_cols}")

        null_counts = self.df[required_columns].isnull().sum().sum()
        if null_counts > 0:
            logger.warning(f"Dataset contains {null_counts} null values. Imputing with median values.")
            self.df[required_columns] = self.df[required_columns].fillna(self.df[required_columns].median())

        logger.info("Schema validation passed successfully.")
        return True

    def get_stratified_splits(
        self, test_size: float = 0.2, val_size: float = 0.1, random_state: int = 42
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Split dataset into train, validation, and test subsets with stratification.
        """
        if self.df is None:
            self.load_raw_data()
        self.validate_schema()

        # Split full -> train_val and test
        train_val_df, test_df = train_test_split(
            self.df, test_size=test_size, random_state=random_state, stratify=self.df['label']
        )

        # Split train_val -> train and val
        relative_val_size = val_size / (1.0 - test_size)
        train_df, val_df = train_test_split(
            train_val_df, test_size=relative_val_size, random_state=random_state, stratify=train_val_df['label']
        )

        logger.info(f"Data Splits Created: Train={len(train_df)}, Val={len(val_df)}, Test={len(test_df)}")
        return train_df, val_df, test_df

if __name__ == "__main__":
    raw_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "ransomware_dataset.csv")
    loader = RansomwareDataLoader(data_path=raw_path)
    train, val, test = loader.get_stratified_splits()
    print("[OK] Data Loader test successful.")
