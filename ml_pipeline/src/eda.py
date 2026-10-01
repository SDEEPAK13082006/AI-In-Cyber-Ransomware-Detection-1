"""
Exploratory Data Analysis (EDA) Module
======================================
Performs statistical profiling, class balance verification, correlation analysis,
and feature distribution analysis for Ransomware Telemetry Datasets.
"""

import os
import json
import logging
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class RansomwareEDA:
    """
    Automated EDA engine for ransomware detection features.
    """
    def __init__(self, data_path: str, output_dir: str):
        self.data_path = data_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.df = pd.read_csv(self.data_path)

    def generate_summary_statistics(self) -> dict:
        """
        Compute descriptive statistics comparing Benign vs Ransomware classes.
        """
        feature_cols = [
            "file_size_kb", "entropy", "num_sections", "has_digital_signature",
            "suspicious_imports", "tls_callbacks_count", "debug_size",
            "shadow_copies_deleted", "registry_run_modified", "file_rename_rate_per_sec",
            "file_modification_entropy_avg", "suspicious_extension_changed",
            "cpu_spike_ratio", "memory_consumption_mb", "network_c2_connections"
        ]

        benign_df = self.df[self.df["label"] == 0]
        malware_df = self.df[self.df["label"] == 1]

        summary = {
            "total_samples": int(len(self.df)),
            "benign_samples": int(len(benign_df)),
            "ransomware_samples": int(len(malware_df)),
            "class_ratio": round(len(malware_df) / len(self.df), 4),
            "family_breakdown": self.df["family"].value_counts().to_dict(),
            "feature_comparisons": {}
        }

        for col in feature_cols:
            summary["feature_comparisons"][col] = {
                "benign": {
                    "mean": float(round(benign_df[col].mean(), 4)),
                    "std": float(round(benign_df[col].std(), 4)),
                    "median": float(round(benign_df[col].median(), 4)),
                    "min": float(round(benign_df[col].min(), 4)),
                    "max": float(round(benign_df[col].max(), 4))
                },
                "ransomware": {
                    "mean": float(round(malware_df[col].mean(), 4)),
                    "std": float(round(malware_df[col].std(), 4)),
                    "median": float(round(malware_df[col].median(), 4)),
                    "min": float(round(malware_df[col].min(), 4)),
                    "max": float(round(malware_df[col].max(), 4))
                }
            }

        report_path = os.path.join(self.output_dir, "eda_summary.json")
        with open(report_path, "w") as f:
            json.dump(summary, f, indent=4)

        logger.info(f"EDA Summary Statistics saved to: {report_path}")
        return summary

    def calculate_correlations(self) -> pd.Series:
        """
        Calculate point biserial correlation between features and the target label.
        """
        feature_cols = [
            "file_size_kb", "entropy", "num_sections", "has_digital_signature",
            "suspicious_imports", "tls_callbacks_count", "debug_size",
            "shadow_copies_deleted", "registry_run_modified", "file_rename_rate_per_sec",
            "file_modification_entropy_avg", "suspicious_extension_changed",
            "cpu_spike_ratio", "memory_consumption_mb", "network_c2_connections"
        ]

        correlations = self.df[feature_cols].apply(lambda col: col.corr(self.df["label"]))
        correlations_sorted = correlations.sort_values(ascending=False)

        corr_path = os.path.join(self.output_dir, "feature_correlations.json")
        with open(corr_path, "w") as f:
            json.dump(correlations_sorted.to_dict(), f, indent=4)

        logger.info(f"Feature Correlations saved to: {corr_path}")
        return correlations_sorted

    def run_full_eda(self) -> dict:
        """
        Run full EDA pipeline and print key insights.
        """
        logger.info("Running Exploratory Data Analysis...")
        summary = self.generate_summary_statistics()
        correlations = self.calculate_correlations()
        
        logger.info("Top Ransomware Predictors (Highest Positive Correlation):")
        for col, val in correlations.items():
            logger.info(f"  - {col:<32}: {val:+.4f}")

        return {
            "summary": summary,
            "correlations": correlations.to_dict()
        }

if __name__ == "__main__":
    raw_csv = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "ransomware_dataset.csv")
    output_reports = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
    
    eda_engine = RansomwareEDA(data_path=raw_csv, output_dir=output_reports)
    eda_results = eda_engine.run_full_eda()
    print("[OK] EDA Phase completed successfully.")
