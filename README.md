# 🛡️ AI-Based Ransomware Detection Platform in Banking Infrastructure
Demo model : https://ransomware-detection-api.onrender.com

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://reactjs.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3-F7931E.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An enterprise-grade, **Pre-Encryption Ransomware Defense Platform** specifically architected for Banking and Financial Institutions. The platform combines static PE binary entropy analysis, dynamic telemetry event tracking, multi-model ensemble machine learning (Random Forest, XGBoost, LightGBM, CatBoost, Isolation Forest), SHAP explainability governance, real-time filesystem watchers, and an interactive React security dashboard.

---

## 📌 Key Architectural Features

1. **Pre-Encryption Detection Engine**: Scans PE binary headers, section Shannon entropy, export/import tables, and Authenticode digital signatures before payload execution.
2. **Dynamic Telemetry Watcher**: Low-latency directory monitoring engine (`watchdog`) tracking shadow copy deletion attempts (`vssadmin`), process creation, and high-frequency extension renames.
3. **Multi-Model Machine Learning Suite**:
   - **Random Forest (Selected Best)**: 100.0% Validation Accuracy, 1.0000 F1-Score.
   - **XGBoost**: Gradient boosted decision tree classification.
   - **LightGBM & CatBoost**: High-throughput multi-class threat classifiers.
   - **Isolation Forest**: Unsupervised anomaly detection baseline trained on benign system activity.
4. **SHAP Explainable AI (XAI)**: Quantifies feature risk contributions (`file_modification_entropy_avg`, `shadow_copies_deleted`, `cpu_spike_ratio`) to eliminate black-box model opacity for security compliance.
5. **Real-time Incident Dispatcher**: Triggers visual security toasts, audible alerts, process quarantine actions, and database audit logs.
6. **Modern Cyber Dashboard**: Built with React, Tailwind CSS, Lucide icons, and Recharts, providing security analysts with live telemetry streams and threat gauges.

---

## 📁 Repository Structure

```
├── Datasets/                      # Banking dataset and network intrusion benchmarks
├── backend/                       # FastAPI REST API Backend
│   └── app/
│       ├── api/v1/endpoints/      # REST API Endpoints (Auth, Detection, Metrics, Monitoring)
│       ├── core/                  # Core configurations, database engine, JWT security, logger
│       ├── models/db/             # SQLAlchemy ORM Models (User, DetectionRecord, AuditLog)
│       ├── schemas/               # Pydantic v2 schemas
│       ├── services/              # ML Predictor, SHAP explainer, Watcher manager, Alert dispatcher
│       └── main.py                # FastAPI Application Entry Point
├── frontend/                      # React Security Command Center UI
│   ├── src/
│   │   ├── components/            # Metric cards, Threat gauges, Live activity streams, Alert center
│   │   ├── context/               # Auth and Theme context providers
│   │   ├── pages/                 # Dashboard, Static Analysis, Realtime Monitor, Model Benchmarks
│   │   └── services/              # Axios API client setup
│   ├── package.json
│   └── vite.config.js
├── ml_pipeline/                   # Machine Learning Engineering Pipeline
│   ├── data/                      # Raw and preprocessed feature numpy matrices
│   ├── models/saved_models/       # Serialized Joblib model binaries
│   └── src/                       # Synthetic generator, Feature engineer, Trainer, SHAP explainer
├── requirements.txt               # Python Dependencies
└── README.md                      # Complete System Documentation
```

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.10+**
- **Node.js 18+** & **npm**

---

### 1. Machine Learning Pipeline Execution

To regenerate the synthetic telemetry dataset, engineer domain features, and train all candidate models:

```bash
# Navigate to workspace root
cd ml_pipeline/src

# Step A: Generate Telemetry Dataset (5000 samples)
python synthetic_dataset_generator.py

# Step B: Perform Feature Engineering & Scaling
python feature_engineering.py

# Step C: Train Multi-Model Suite & Select Best Model
python train.py
```

---

### 2. Backend FastAPI Server Startup

To launch the FastAPI REST API backend with SQLite database auto-initialization:

```bash
# From repository root
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

- **Interactive API Documentation (Swagger)**: `http://localhost:8000/api/v1/docs`
- **ReDoc Documentation**: `http://localhost:8000/api/v1/redoc`

---

### 3. Frontend React Command Center

To run the security dashboard interface:

```bash
cd frontend

# Install Node dependencies
npm install

# Launch Development Server
npm run dev
```

Open browser at `http://localhost:3000` (or `http://localhost:5173`).

### 4. Deploy the Frontend to Vercel

The React dashboard can be deployed on Vercel as a static site. The frontend is configured to read the backend API base URL from `VITE_API_BASE_URL`.

1. In the Vercel dashboard, create a new project and select this repository.
2. Set the build command to `npm run build` and the output directory to `dist`.
3. Add an environment variable:
   - `VITE_API_BASE_URL` = `https://<your-backend-host>/api/v1`
4. Deploy the project.

> Note: The Python FastAPI backend must be hosted separately. Vercel is configured here for the static React frontend only.

---

## 📊 Model Performance Benchmarks

Empirical validation results on test split (20% holdout):

| Algorithm | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Random Forest** | **100.0%** | **100.0%** | **100.0%** | **1.0000** | **1.0000** | ⭐ **SELECTED BEST** |
| **XGBoost** | 100.0% | 100.0% | 100.0% | 1.0000 | 1.0000 | DEPLOYED |
| **LightGBM** | 100.0% | 100.0% | 100.0% | 1.0000 | 1.0000 | READY |
| **CatBoost** | 100.0% | 100.0% | 100.0% | 1.0000 | 1.0000 | READY |
| **Isolation Forest** | 74.0% | 70.2% | 91.4% | 0.7937 | 1.0000 | ANOMALY BASELINE |

---

## 🛠️ API Endpoint Summary

- **`POST /api/v1/auth/login`**: Authenticate security analyst & generate JWT token.
- **`POST /api/v1/auth/register`**: Register security analyst account.
- **`POST /api/v1/detection/analyze`**: Single file PE entropy analysis & SHAP explanation.
- **`POST /api/v1/detection/batch`**: Directory batch threat evaluation.
- **`GET /api/v1/metrics/summary`**: High-level dashboard threat velocity metrics.
- **`GET /api/v1/metrics/models`**: Comparative machine learning model benchmarks.
- **`GET /api/v1/monitoring/live-logs`**: Real-time process telemetry activity log stream.
- **`GET/POST /api/v1/monitoring/watchers`**: Manage filesystem watchdog directories.

---

## 📜 License & Compliance

Distributed under the **MIT License**. Designed for security evaluation and threat research in financial systems.
