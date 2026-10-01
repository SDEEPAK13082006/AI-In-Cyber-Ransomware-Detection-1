"""
Comprehensive Multi-Dataset Model Training Pipeline
===================================================
Trains:
1. Pre-Encryption Ransomware Behavioral & Telemetry Models (Random Forest, XGBoost, LightGBM, CatBoost, Isolation Forest)
2. Obfuscated Malware Memory Dump Classifier (MalMem2022)
3. Network Intrusion & C2 Attack Classifier (ISCX / PCAP)

Exports all models as .pkl files to:
- models/
- ml_pipeline/models/saved_models/
- ml_pipeline/data/processed/
"""

import os
import sys
import pickle
import json
import logging
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from xgboost import XGBClassifier

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

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger("train_datasets")

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

MODELS_DIR = os.path.join(ROOT_DIR, "models")
ML_SAVED_MODELS_DIR = os.path.join(ROOT_DIR, "ml_pipeline", "models", "saved_models")
PROCESSED_DIR = os.path.join(ROOT_DIR, "ml_pipeline", "data", "processed")
RAW_DATA_PATH = os.path.join(ROOT_DIR, "ml_pipeline", "data", "raw", "ransomware_dataset.csv")
DATASETS_DIR = os.path.join(ROOT_DIR, "Datasets")

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(ML_SAVED_MODELS_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

def save_pickle_artifacts(filename_base: str, obj: any):
    """Save artifact in both models/ and ml_pipeline/models/saved_models/ as .pkl."""
    path1 = os.path.join(MODELS_DIR, f"{filename_base}.pkl")
    path2 = os.path.join(ML_SAVED_MODELS_DIR, f"{filename_base}.pkl")
    
    with open(path1, "wb") as f:
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    with open(path2, "wb") as f:
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    
    logger.info(f"Saved: {path1} and {path2}")

# =========================================================================
# Part 1: Train Ransomware Pre-Encryption & Telemetry Models
# =========================================================================
def train_ransomware_models():
    logger.info("=== [1/3] Training Ransomware Telemetry Models ===")
    
    # Check if raw dataset exists, if not generate it
    if not os.path.exists(RAW_DATA_PATH):
        logger.info("Raw dataset not found. Generating synthetic telemetry dataset...")
        from ml_pipeline.src.synthetic_dataset_generator import generate_synthetic_dataset
        df = generate_synthetic_dataset(num_samples=5000)
        os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)
        df.to_csv(RAW_DATA_PATH, index=False)
    else:
        df = pd.read_csv(RAW_DATA_PATH)

    from ml_pipeline.src.feature_engineering import FeatureEngineer
    fe = FeatureEngineer()
    
    train_val_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['label'])
    train_df, val_df = train_test_split(train_val_df, test_size=0.125, random_state=42, stratify=train_val_df['label'])
    
    X_train, y_train = fe.fit_transform(train_df)
    X_val, y_val = fe.transform(val_df)
    X_test, y_test = fe.transform(test_df)
    
    # Save feature scaler & metadata
    scaler_payload = {"scaler": fe.scaler, "selector": fe.variance_selector}
    save_pickle_artifacts("feature_scaler", scaler_payload)
    with open(os.path.join(PROCESSED_DIR, "feature_scaler.pkl"), "wb") as f:
        pickle.dump(scaler_payload, f)

    with open(os.path.join(MODELS_DIR, "feature_names.json"), "w") as f:
        json.dump(fe.feature_names, f, indent=4)
    with open(os.path.join(PROCESSED_DIR, "feature_names.json"), "w") as f:
        json.dump(fe.feature_names, f, indent=4)

    # Candidate models
    candidates = {
        "randomforest_model": RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1),
        "xgboost_model": XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, eval_metric="logloss"),
        "isolationforest_model": IsolationForest(n_estimators=100, contamination=0.5, random_state=42, n_jobs=-1)
    }

    if HAS_LGBM:
        candidates["lightgbm_model"] = LGBMClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, verbose=-1)
    if HAS_CATBOOST:
        candidates["catboost_model"] = CatBoostClassifier(iterations=150, depth=6, learning_rate=0.1, verbose=0, random_seed=42)

    benchmark_results = {}
    best_f1 = -1.0
    best_name = "randomforest_model"
    best_obj = None

    for name, model in candidates.items():
        logger.info(f"Training [{name}]...")
        if "isolationforest" in name:
            benign_mask = (y_train == 0)
            model.fit(X_train[benign_mask])
            raw_preds = model.predict(X_val)
            y_pred = np.where(raw_preds == -1, 1, 0)
            y_probs = -model.decision_function(X_val)
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_val)
            y_probs = model.predict_proba(X_val)[:, 1]

        acc = float(accuracy_score(y_val, y_pred))
        prec = float(precision_score(y_val, y_pred, zero_division=0))
        rec = float(recall_score(y_val, y_pred, zero_division=0))
        f1 = float(f1_score(y_val, y_pred, zero_division=0))
        auc = float(roc_auc_score(y_val, y_probs))

        benchmark_results[name] = {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "roc_auc": round(auc, 4)
        }
        logger.info(f" -> {name} | Accuracy: {acc:.4f} | F1: {f1:.4f} | AUC: {auc:.4f}")
        
        # Save each model as .pkl
        save_pickle_artifacts(name, model)

        if f1 > best_f1:
            best_f1 = f1
            best_name = name
            best_obj = model

    # Save best model
    best_payload = {
        "model_name": best_name.replace("_model", ""),
        "model": best_obj,
        "metrics": benchmark_results[best_name]
    }
    save_pickle_artifacts("best_ransomware_model", best_payload)
    
    with open(os.path.join(MODELS_DIR, "model_benchmark_results.json"), "w") as f:
        json.dump({"best_model": best_name, "benchmark": benchmark_results}, f, indent=4)
    with open(os.path.join(PROCESSED_DIR, "model_benchmark_results.json"), "w") as f:
        json.dump({"best_model": best_name, "benchmark": benchmark_results}, f, indent=4)

    logger.info("Ransomware models successfully trained and saved as .pkl!")

# =========================================================================
# Part 2: Train Obfuscated Malware & Ransomware Memory Dump Model (MalMem2022)
# =========================================================================
def train_malmem_model():
    logger.info("=== [2/3] Training MalMem2022 Memory Malware Detector ===")
    malmem_path = os.path.join(DATASETS_DIR, "Obfuscated-MalMem2022.csv")
    if not os.path.exists(malmem_path):
        logger.warning(f"MalMem dataset not found at {malmem_path}. Skipping.")
        return

    logger.info(f"Loading {malmem_path}...")
    df = pd.read_csv(malmem_path)
    logger.info(f"Loaded {len(df)} records.")

    target_col = "Class" if "Class" in df.columns else df.columns[-1]
    
    drop_cols = ["Category", "Class", target_col]
    feature_cols = [c for c in df.columns if c not in drop_cols and np.issubdtype(df[c].dtype, np.number)]
    
    X = df[feature_cols].fillna(0).values
    le = LabelEncoder()
    y = le.fit_transform(df[target_col].astype(str))

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)

    logger.info(f"Training MalMem RandomForest on {len(feature_cols)} memory features...")
    rf_malmem = RandomForestClassifier(n_estimators=100, max_depth=14, random_state=42, n_jobs=-1)
    rf_malmem.fit(X_train, y_train)

    y_pred = rf_malmem.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    logger.info(f"MalMem Model Accuracy: {acc:.4f} | F1: {f1:.4f}")

    save_pickle_artifacts("malmem_randomforest_model", rf_malmem)
    save_pickle_artifacts("malmem_scaler", {
        "scaler": scaler,
        "feature_names": feature_cols,
        "classes": le.classes_.tolist()
    })
    logger.info("MalMem2022 model saved successfully as .pkl!")

# =========================================================================
# Part 3: Train Network Intrusion & C2 Attack Classifier
# =========================================================================
def train_network_intrusion_model():
    logger.info("=== [3/3] Training Network Intrusion & C2 Threat Classifier ===")
    pcap_files = [
        "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv",
        "Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv",
        "Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv"
    ]
    
    frames = []
    for pf in pcap_files:
        full_path = os.path.join(DATASETS_DIR, pf)
        if os.path.exists(full_path):
            logger.info(f"Sampling 10,000 rows from {pf}...")
            sample = pd.read_csv(full_path, nrows=10000)
            frames.append(sample)

    if not frames:
        logger.warning("No PCAP dataset files found. Skipping.")
        return

    df_net = pd.concat(frames, ignore_index=True)
    df_net.columns = df_net.columns.str.strip()
    
    target_col = "Label" if "Label" in df_net.columns else df_net.columns[-1]
    
    drop_cols = ["Label", target_col]
    num_cols = [c for c in df_net.columns if c not in drop_cols and np.issubdtype(df_net[c].dtype, np.number)]
    
    df_clean = df_net[num_cols + [target_col]].replace([np.inf, -np.inf], np.nan).dropna()
    
    X = df_clean[num_cols].values
    y = np.where(df_clean[target_col].astype(str).str.upper() == 'BENIGN', 0, 1)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)

    logger.info(f"Training Network Threat Classifier on {len(num_cols)} flow features...")
    rf_net = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1)
    rf_net.fit(X_train, y_train)

    y_pred = rf_net.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    logger.info(f"Network Threat Model Accuracy: {acc:.4f} | F1: {f1:.4f}")

    save_pickle_artifacts("network_threat_model", rf_net)
    save_pickle_artifacts("network_scaler", {
        "scaler": scaler,
        "feature_names": num_cols
    })
    logger.info("Network Threat Classifier saved successfully as .pkl!")

if __name__ == "__main__":
    logger.info("Starting complete multi-dataset training and .pkl artifact generation...")
    train_ransomware_models()
    train_malmem_model()
    train_network_intrusion_model()
    logger.info("=== [ALL DONE] All datasets trained and .pkl files saved to models/ folder! ===")
