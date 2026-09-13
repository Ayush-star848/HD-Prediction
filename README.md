# ❤️ CardioSense AI

> **AI-powered heart disease risk prediction platform using multiple machine learning models and a soft-voting ensemble.**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-black.svg)](https://flask.palletsprojects.com/)
[![Scikit--Learn](https://img.shields.io/badge/scikit--learn-1.4.2-orange.svg)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0.3-red.svg)](https://xgboost.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#-license)

**CardioSense AI** is a full-stack machine learning application designed to assess heart disease risk from commonly used cardiovascular health parameters.

The platform combines **8 individual machine learning models** with a **soft-voting ensemble**, providing model-level predictions, an overall risk score, risk classification, risk-factor identification, and personalized health recommendations.

It also supports **bulk prediction through CSV uploads**, making it possible to analyze multiple patient records in a single request.

🌐 **Live Demo:** https://cardiosense-ai-q5wf.onrender.com/

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Project Highlights](#-project-highlights)
- [System Architecture](#-system-architecture)
- [Project Structure](#-project-structure)
- [Machine Learning Models](#-machine-learning-models)
- [Dataset & Training](#-dataset--training)
- [Prediction Workflow](#-prediction-workflow)
- [Input Parameters](#-input-parameters)
- [Risk Classification](#-risk-classification)
- [Personalized Recommendations](#-personalized-recommendations)
- [Bulk Prediction Workflow](#-bulk-prediction-workflow)
- [Bulk CSV Format](#-bulk-csv-format)
- [API Documentation](#-api-documentation)
- [API Examples](#-api-examples)
- [Validation & Error Handling](#-validation--error-handling)
- [Frontend](#-frontend)
- [Testing](#-testing)
- [Getting Started](#-getting-started)
- [Model Training](#-model-training)
- [Deployment](#-deployment)
- [Environment Configuration](#-environment-configuration)
- [Tech Stack](#-tech-stack)
- [Dependencies](#-dependencies)
- [Key Components](#-key-components)
- [Future Improvements](#-future-improvements)
- [Medical Disclaimer](#-medical-disclaimer)
- [Contributors](#-contributors)
- [License](#-license)

---

# 🩺 Overview

CardioSense AI provides a simple interface for evaluating cardiovascular risk using patient health information.

The application accepts **13 input features** and passes them through a validation and machine learning pipeline.

For an individual assessment, the system can:

1. Validate the submitted patient data.
2. Convert the inputs into a machine learning feature vector.
3. Run the selected machine learning models.
4. Generate model-level predictions and probabilities.
5. Calculate an ensemble risk score.
6. Classify the patient into a risk tier.
7. Identify potential risk factors.
8. Generate personalized recommendations.
9. Produce a detailed health action plan.

The platform also provides a dedicated bulk analysis workflow where users can upload a CSV containing **10–500 patient records** and receive predictions for all valid records.

---

# ✨ Features

## 🤖 Machine Learning

- Multiple classification algorithms.
- 8 individual machine learning models.
- Soft-voting ensemble model.
- Probability-based prediction.
- Model-level prediction comparison.
- Best-performing model identification.
- Persisted trained models using `joblib`.
- Standard scaling for models that require feature normalization.

## 📊 Individual Patient Prediction

- Interactive patient assessment form.
- 13 cardiovascular input parameters.
- Input validation and sanitization.
- Selectable machine learning models.
- Overall ensemble probability.
- Low / Medium / High risk classification.
- Individual model predictions.
- Best model information.

## 📁 Bulk Patient Analysis

- CSV file upload.
- Supports **10–500 patient records**.
- Automatic column normalization.
- Required-column validation.
- Batch prediction using the Voting Ensemble.
- Invalid row detection.
- Patient-level prediction results.
- Aggregate statistics including:
  - Total patients
  - Positive cases
  - Negative cases
  - High-risk cases
  - Medium-risk cases
  - Low-risk cases
  - Average probability

## 📋 Detailed Health Report

The application generates a detailed action plan containing:

- Risk summary.
- Risk score.
- Risk factors.
- Immediate actions.
- Lifestyle recommendations.
- Things to avoid.
- Warning signs.
- Follow-up schedule.
- Clinical recommendations.

## 🎨 Modern Frontend

- Responsive web interface.
- Dark / light theme.
- Dashboard-style UI.
- Responsive patient assessment form.
- Bulk upload interface.
- Detailed results page.
- Printable action plan.
- Modern typography using:
  - Syne
  - Instrument Serif
  - JetBrains Mono

## 🔒 Backend Validation

The API validates:

- Required fields.
- Numeric types.
- Minimum and maximum ranges.
- Allowed categorical values.
- Selected model names.
- CSV structure.
- CSV row limits.
- File type.

---

# 🌟 Project Highlights

| Capability | Implementation |
|---|---|
| Web Framework | Flask |
| ML Framework | Scikit-learn + XGBoost |
| Individual Prediction | ✅ |
| Multi-model Prediction | ✅ |
| Voting Ensemble | ✅ |
| Bulk CSV Prediction | ✅ |
| Input Validation | ✅ |
| Risk Classification | ✅ |
| Health Recommendations | ✅ |
| Detailed Action Plan | ✅ |
| REST API | ✅ |
| Health Check | ✅ |
| Model Metadata API | ✅ |
| Automated Tests | ✅ |
| Production Deployment | ✅ |

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────────┐
                         │       User / Client     │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │       Flask App         │
                         │       backend/app.py    │
                         └────────────┬────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
                    ▼                 ▼                 ▼
             ┌────────────┐   ┌──────────────┐   ┌──────────────┐
             │ Page Routes│   │ Prediction   │   │ Bulk Routes  │
             │   pages.py │   │   predict.py │   │   bulk.py    │
             └────────────┘   └──────┬───────┘   └──────┬───────┘
                                      │                  │
                                      ▼                  ▼
                              ┌──────────────────────────────┐
                              │       Validation Layer       │
                              │       validators.py          │
                              └──────────────┬───────────────┘
                                             │
                                             ▼
                              ┌──────────────────────────────┐
                              │      Prediction Engine       │
                              │       predictor.py            │
                              └──────────────┬───────────────┘
                                             │
                    ┌────────────────────────┼────────────────────────┐
                    │                        │                        │
                    ▼                        ▼                        ▼
             ┌────────────┐          ┌────────────┐          ┌────────────┐
             │ Individual │          │ Individual │          │   Voting   │
             │   Models   │          │   Models   │          │  Ensemble  │
             └────────────┘          └────────────┘          └────────────┘
                                             │
                                             ▼
                              ┌──────────────────────────────┐
                              │       Risk Classification    │
                              │        Low / Medium / High   │
                              └──────────────┬───────────────┘
                                             │
                                             ▼
                              ┌──────────────────────────────┐
                              │ Recommendations & Summary    │
                              │      recommendations.py      │
                              └──────────────┬───────────────┘
                                             │
                                             ▼
                              ┌──────────────────────────────┐
                              │       Frontend Results       │
                              │     Action Plan / Summary    │
                              └──────────────────────────────┘
```

---

# 📂 Project Structure

```text
CardioSense/
│
├── backend/
│   ├── __init__.py
│   ├── app.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── predictor.py
│   │   └── trainer.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── pages.py
│   │   ├── predict.py
│   │   ├── bulk.py
│   │   └── health.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── validators.py
│       └── recommendations.py
│
├── data/
│   └── models/
│       ├── scaler.pkl
│       ├── logistic_regression.pkl
│       ├── random_forest.pkl
│       ├── svm.pkl
│       ├── xgboost.pkl
│       ├── gradient_boosting.pkl
│       ├── knn.pkl
│       ├── naive_bayes.pkl
│       ├── decision_tree.pkl
│       └── voting_ensemble.pkl
│
├── frontend/
│   ├── templates/
│   │   ├── index.html
│   │   ├── bulk.html
│   │   └── summary.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       │
│       └── js/
│           ├── app.js
│           └── bulk.js
│
├── tests/
│   ├── __init__.py
│   ├── test_routes.py
│   └── test_validators.py
│
├── .gitignore
├── Procfile
├── README.md
├── requirements.txt
├── run.py
└── runtime.txt
```

---

# 🧠 Machine Learning Models

CardioSense uses multiple classification algorithms to provide a broader prediction comparison.

| Model | Reported Accuracy |
|---|---:|
| ⭐ Voting Ensemble | **96%** |
| XGBoost | **95%** |
| Gradient Boosting | **94%** |
| Random Forest | **93%** |
| Support Vector Machine | **91%** |
| Logistic Regression | **86%** |
| K-Nearest Neighbors | **85%** |
| Decision Tree | **84%** |
| Naïve Bayes | **82%** |

> **Note:** The accuracy values shown above are the model metadata currently configured in the application. Actual performance depends on the training data, split, preprocessing, and evaluation methodology.

---

# 🔬 Dataset & Training

The training pipeline is implemented in:

```text
backend/models/trainer.py
```

The project currently generates a **synthetic Cleveland-mirrored dataset** for training and experimentation.

The generated dataset contains:

- 1,200 records by default.
- 13 input features.
- A binary target variable.
- A clinically inspired risk-scoring mechanism.
- Small random noise to prevent completely deterministic labels.

The default dataset generation is controlled using a fixed random seed:

```python
generate_data(n=1200, seed=42)
```

This makes the training process reproducible.

---

## Training Process

The training pipeline performs:

```text
Dataset Generation
       │
       ▼
Feature / Target Separation
       │
       ▼
Stratified Train/Test Split
       │
       ▼
StandardScaler
       │
       ▼
Individual Model Training
       │
       ▼
Test Accuracy Evaluation
       │
       ▼
5-Fold Cross Validation
       │
       ▼
Top 4 Models Selected
       │
       ▼
Soft Voting Ensemble
       │
       ▼
Persist Models with Joblib
```

---

# 🔮 Prediction Workflow

CardioSense's individual prediction workflow follows this process:

```text
Patient Input
      │
      ▼
Input Validation
      │
      ▼
Data Sanitization
      │
      ▼
Feature Vector Creation
      │
      ▼
Selected ML Models
      │
      ├───────────────┐
      ▼               ▼
Individual Models   Voting Ensemble
      │               │
      └───────┬───────┘
              ▼
       Probability Scores
              │
              ▼
       Ensemble Risk Score
              │
              ▼
       Risk Classification
              │
              ▼
     Risk Factors & Insights
              │
              ▼
      Recommendations
              │
              ▼
       Detailed Summary
```

---

# 🧮 Ensemble Prediction

The ensemble prediction engine collects probability estimates from the selected models.

For the ensemble risk score, the application calculates the average probability:

```text
Ensemble Probability =
    Average(probability from selected models)
```

The resulting score is then used to classify the patient's risk level.

The ensemble prediction threshold is:

```text
Probability >= 50%
        │
        ├── 1 → Disease Predicted
        │
        └── 0 → No Disease Predicted
```

---

# 🚦 Risk Classification

CardioSense categorizes the calculated risk score into three tiers:

| Risk Score | Risk Tier |
|---:|---|
| `< 40%` | 🟢 Low |
| `40% – 64%` | 🟡 Medium |
| `>= 65%` | 🔴 High |

These thresholds are application-level classification rules and should not be interpreted as validated clinical risk thresholds.

---

# 📝 Input Parameters

CardioSense accepts the following 13 features:

| Feature | Description | Validation |
|---|---|---|
| `age` | Patient age | 18–100 |
| `sex` | Sex encoding | 0 or 1 |
| `cp` | Chest pain type | 0–3 |
| `trestbps` | Resting blood pressure | 80–220 |
| `chol` | Serum cholesterol | 100–600 |
| `fbs` | Fasting blood sugar indicator | 0 or 1 |
| `restecg` | Resting ECG result | 0–2 |
| `thalach` | Maximum heart rate achieved | 60–220 |
| `exang` | Exercise-induced angina | 0 or 1 |
| `oldpeak` | ST depression | 0.0–6.2 |
| `slope` | ST segment slope | 0–2 |
| `ca` | Number of major vessels | 0–3 |
| `thal` | Thalassemia-related categorical value | 1–3 |

---

# 💡 Personalized Recommendations

After prediction, CardioSense generates recommendations based on the patient's:

- Risk tier.
- Blood pressure.
- Cholesterol.
- Blood sugar indicator.
- Exercise-induced angina.
- ST depression.
- Vessel-related features.
- Thalassemia-related feature.
- Age.
- Other detected risk factors.

The recommendation engine is implemented in:

```text
backend/utils/recommendations.py
```

Recommendations may include:

- Heart-healthy dietary guidance.
- Physical activity guidance.
- Blood pressure management.
- Cholesterol management.
- Smoking avoidance.
- Sleep and stress management.
- Follow-up suggestions.
- Warning signs requiring urgent attention.

---

# 📋 Detailed Action Plan

The summary page provides a structured report with the following sections:

```text
01  Risk Factors Identified
02  Immediate Actions
03  What To Do
04  What To Avoid
05  Warning Signs
06  Follow-up Schedule
07  Clinical Recommendations
```

The report is rendered using:

```text
frontend/templates/summary.html
```

The application also supports printing the generated action plan directly from the browser.

---

# 📁 Bulk Prediction Workflow

CardioSense supports batch analysis through:

```text
POST /api/bulk
```

The bulk workflow is:

```text
CSV Upload
    │
    ▼
File Type Validation
    │
    ▼
CSV Parsing
    │
    ▼
Column Normalisation
    │
    ▼
Required Column Validation
    │
    ▼
Row Count Validation
    │
    ▼
Record Conversion
    │
    ▼
Voting Ensemble Prediction
    │
    ▼
Patient-Level Results
    │
    ▼
Aggregate Statistics
```

The system accepts:

```text
Minimum records: 10
Maximum records: 500
Maximum upload size: 10 MB
```

Invalid rows are identified separately rather than causing the entire batch to fail.

---

# 📄 Bulk CSV Format

The CSV must contain the following columns:

```csv
age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal
```

Example:

```csv
age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal
63,1,3,145,233,1,0,150,0,2.3,0,0,1
55,1,2,140,250,0,1,140,1,2.3,1,1,3
48,0,1,120,210,0,0,170,0,0.5,1,0,2
```

### CSV Requirements

- File must have a `.csv` extension.
- Column names are normalized to lowercase.
- All required columns must be present.
- The file must contain between **10 and 500 rows**.
- Each row should contain numeric values compatible with the expected feature format.

---

# 🔌 API Documentation

## `GET /`

Returns the main CardioSense prediction dashboard.

### Response

HTML page.

---

## `GET /bulk`

Returns the bulk CSV analysis page.

### Response

HTML page.

---

## `GET /summary`

Returns the detailed patient summary stored in the current Flask session.

### Response

HTML page.

---

## `POST /api/predict`

Performs an individual patient prediction.

### Request

```json
{
  "age": 55,
  "sex": 1,
  "cp": 3,
  "trestbps": 140,
  "chol": 250,
  "fbs": 0,
  "restecg": 1,
  "thalach": 140,
  "exang": 1,
  "oldpeak": 2.3,
  "slope": 1,
  "ca": 1,
  "thal": 3
}
```

An optional `selected_models` list can be supplied:

```json
{
  "age": 55,
  "sex": 1,
  "cp": 3,
  "trestbps": 140,
  "chol": 250,
  "fbs": 0,
  "restecg": 1,
  "thalach": 140,
  "exang": 1,
  "oldpeak": 2.3,
  "slope": 1,
  "ca": 1,
  "thal": 3,
  "selected_models": [
    "xgboost",
    "random_forest",
    "voting_ensemble"
  ]
}
```

### Successful Response

```json
{
  "success": true,
  "model_results": [],
  "ensemble_prob": 72,
  "ensemble_pred": 1,
  "risk_tier": "high",
  "positive_count": 3,
  "total_models": 3,
  "best_model": {},
  "recommendations": [],
  "summary": {}
}
```

---

## `POST /api/store-summary`

Stores summary data in the Flask session for rendering on the summary page.

### Request

```json
{
  "risk_tier": "medium",
  "probability": 52
}
```

### Response

```json
{
  "success": true
}
```

---

## `POST /api/bulk`

Accepts a CSV file and performs batch prediction using the Voting Ensemble.

### Request

```text
Content-Type: multipart/form-data
```

File field:

```text
file
```

### Successful Response

```json
{
  "success": true,
  "total_patients": 100,
  "positive_cases": 42,
  "negative_cases": 58,
  "high_risk": 20,
  "medium_risk": 35,
  "low_risk": 45,
  "avg_probability": 43.7,
  "invalid_rows": [],
  "model_used": "Voting Ensemble",
  "results": []
}
```

---

## `GET /api/health`

Provides an application health check.

### Example Response

```json
{
  "status": "ok",
  "models_ready": true,
  "message": "All systems operational."
}
```

If trained models are unavailable:

```json
{
  "status": "degraded",
  "models_ready": false,
  "message": "Run: python -m backend.models.trainer"
}
```

---

## `GET /api/models`

Returns metadata for all supported models.

### Example

```json
{
  "models": {
    "logistic_regression": {
      "name": "Logistic Regression",
      "accuracy": 86,
      "trained": true
    },
    "random_forest": {
      "name": "Random Forest",
      "accuracy": 93,
      "trained": true
    }
  }
}
```

---

# 🧪 API Examples

## Using cURL

### Individual Prediction

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 55,
    "sex": 1,
    "cp": 3,
    "trestbps": 140,
    "chol": 250,
    "fbs": 0,
    "restecg": 1,
    "thalach": 140,
    "exang": 1,
    "oldpeak": 2.3,
    "slope": 1,
    "ca": 1,
    "thal": 3
  }'
```

### Health Check

```bash
curl http://localhost:5000/api/health
```

### Model Metadata

```bash
curl http://localhost:5000/api/models
```

### Bulk Prediction

```bash
curl -X POST http://localhost:5000/api/bulk \
  -F "file=@patients.csv"
```

---

# 🛡️ Validation & Error Handling

CardioSense uses a dedicated validation layer:

```text
backend/utils/validators.py
```

The validation system checks:

### Required Fields

All 13 patient features must be present.

### Data Types

Integer and floating-point values are converted and validated before prediction.

### Range Validation

Each feature is checked against its accepted range.

### Categorical Validation

Categorical variables are checked against their allowed values.

### Model Selection

If `selected_models` is provided, every model name must belong to the supported model set.

Supported model keys:

```text
logistic_regression
random_forest
svm
xgboost
gradient_boosting
knn
naive_bayes
decision_tree
voting_ensemble
```

---

# ❌ API Error Responses

### Invalid JSON

```http
400 Bad Request
```

```json
{
  "success": false,
  "error": "Invalid JSON body"
}
```

### Validation Error

```http
422 Unprocessable Entity
```

```json
{
  "success": false,
  "errors": [
    "Missing required field: 'age'"
  ]
}
```

### Missing Models

```http
503 Service Unavailable
```

The API instructs the developer to train the models:

```bash
python -m backend.models.trainer
```

---

# 🎨 Frontend

The frontend is built using standard web technologies without a frontend framework.

## Technologies

- HTML5
- CSS3
- JavaScript ES6
- Jinja2 templates

## Main Pages

### Assessment Dashboard

```text
frontend/templates/index.html
```

Used for:

- Patient data entry.
- Model selection.
- Prediction requests.
- Displaying prediction results.

### Bulk Analysis

```text
frontend/templates/bulk.html
```

Used for:

- CSV upload.
- Batch analysis.
- Result visualization.
- Patient-level result display.

### Summary / Action Plan

```text
frontend/templates/summary.html
```

Used for:

- Detailed risk report.
- Risk factors.
- Recommendations.
- Follow-up plan.
- Warning signs.
- Printable report.

---

# 🧪 Testing

The project includes automated tests using `pytest`.

Test files:

```text
tests/
├── test_routes.py
└── test_validators.py
```

Run all tests:

```bash
python -m pytest tests/ -v
```

---

## Current Test Coverage

The test suite covers important application behavior including:

- Health endpoint.
- Model metadata endpoint.
- Missing prediction fields.
- Invalid JSON.
- Main page rendering.
- Bulk endpoint without file.
- Valid input validation.
- Missing fields.
- Out-of-range values.
- Invalid categorical values.
- String-to-number coercion.
- Valid model selection.
- Invalid model selection.

---

# 🚀 Getting Started

## Prerequisites

Make sure you have:

- Python 3.11+
- Git
- pip

---

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/cardiosense.git
```

Navigate into the project:

```bash
cd cardiosense
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Train the Models

If the `.pkl` model files are not available or need to be regenerated:

```bash
python -m backend.models.trainer
```

This creates the trained model files inside:

```text
data/models/
```

---

## 5. Start the Application

```bash
python run.py
```

The application will run on:

```text
http://localhost:5000
```

Open the address in your browser.

---

# 🧠 Model Training

The training script can be executed with:

```bash
python -m backend.models.trainer
```

The script:

1. Generates the training dataset.
2. Separates features and target.
3. Creates a stratified train/test split.
4. Fits a `StandardScaler`.
5. Trains all individual models.
6. Calculates test accuracy.
7. Performs 5-fold cross-validation.
8. Selects the top four models.
9. Creates a soft-voting ensemble.
10. Saves all trained models using `joblib`.

---

## Saved Model Files

The following files are generated:

```text
data/models/
│
├── scaler.pkl
├── logistic_regression.pkl
├── random_forest.pkl
├── svm.pkl
├── xgboost.pkl
├── gradient_boosting.pkl
├── knn.pkl
├── naive_bayes.pkl
├── decision_tree.pkl
└── voting_ensemble.pkl
```

---

# 🌐 Deployment

CardioSense AI is deployed as a production web application.

### Live Application

🌐 **https://cardiosense-ai-q5wf.onrender.com/**

The project includes a `Procfile` configured for Gunicorn:

```text
web: gunicorn run:app --workers 2 --bind 0.0.0.0:$PORT
```

The project specifies Python 3.11.9 through:

```text
runtime.txt
```

```text
python-3.11.9
```

---

# ⚙️ Environment Configuration

The Flask application supports an optional environment variable:

```text
SECRET_KEY
```

If it is not supplied, the application falls back to a development default.

For production deployments, set your own secure secret key.

Example:

```text
SECRET_KEY=your-secure-secret-key
```

---

# 📦 Dependencies

The project's primary dependencies are:

| Package | Version |
|---|---:|
| Flask | 3.0.3 |
| Flask-CORS | 4.0.1 |
| Scikit-learn | 1.4.2 |
| XGBoost | 2.0.3 |
| NumPy | 1.26.4 |
| Pandas | 2.2.2 |
| Joblib | 1.4.2 |
| Python-dotenv | 1.0.1 |
| Gunicorn | 22.0.0 |

Install everything with:

```bash
pip install -r requirements.txt
```

---

# 🛠️ Tech Stack

## Backend

- Python
- Flask
- Flask-CORS
- Gunicorn

## Machine Learning

- Scikit-learn
- XGBoost
- NumPy
- Pandas
- Joblib

## Frontend

- HTML5
- CSS3
- JavaScript
- Jinja2

## Testing

- Pytest

## Deployment

- Gunicorn
- Render

---

# 🧩 Key Components

## `backend/app.py`

Application factory responsible for:

- Creating the Flask application.
- Configuring templates and static files.
- Configuring CORS.
- Registering application blueprints.
- Setting upload limits.
- Configuring the Flask secret key.

---

## `backend/models/trainer.py`

Responsible for:

- Dataset generation.
- Model configuration.
- Training.
- Evaluation.
- Cross-validation.
- Ensemble creation.
- Model persistence.

---

## `backend/models/predictor.py`

Responsible for:

- Loading trained models.
- Loading the scaler.
- Converting patient inputs to feature vectors.
- Running individual predictions.
- Calculating ensemble predictions.
- Calculating risk tiers.
- Running batch predictions.

The predictor uses a singleton instance:

```python
predictor = HeartDiseasePredictor()
```

This allows trained models to be loaded once and reused across requests.

---

## `backend/utils/validators.py`

Responsible for:

- Input validation.
- Type conversion.
- Range checks.
- Categorical checks.
- Model selection validation.
- Sanitized input generation.

---

## `backend/utils/recommendations.py`

Responsible for:

- Risk factor identification.
- Personalized recommendations.
- Immediate action suggestions.
- Lifestyle recommendations.
- Warning signs.
- Follow-up schedules.
- Detailed action-plan generation.

---

## `backend/routes/predict.py`

Provides:

```text
POST /api/predict
POST /api/store-summary
```

Responsible for:

- Single-patient prediction.
- Validation.
- Model execution.
- Recommendation generation.
- Summary generation.
- Session storage.

---

## `backend/routes/bulk.py`

Provides:

```text
POST /api/bulk
```

Responsible for:

- CSV uploads.
- CSV validation.
- Batch prediction.
- Invalid row tracking.
- Aggregate statistics.

---

## `backend/routes/health.py`

Provides:

```text
GET /api/health
GET /api/models
```

Responsible for:

- Application health checks.
- Model readiness checks.
- Model metadata.

---

## `frontend/`

Contains the complete web interface:

```text
frontend/
├── templates/
│   ├── index.html
│   ├── bulk.html
│   └── summary.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    └── js/
        ├── app.js
        └── bulk.js
```

---

# 🔄 End-to-End Architecture

```text
                    ┌──────────────────┐
                    │      Browser     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │      Flask       │
                    │   Application    │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
         Page Routes    Prediction API   Bulk API
              │              │              │
              │              ▼              ▼
              │        Validation       CSV Validation
              │              │              │
              │              ▼              ▼
              │       Predictor Engine  Batch Predictor
              │              │              │
              │              ▼              │
              │       ML Model Layer        │
              │              │              │
              │              ▼              ▼
              │       Ensemble Prediction
              │              │
              └──────────────┤
                             ▼
                    Risk Classification
                             │
                             ▼
                  Recommendation Engine
                             │
                             ▼
                    Detailed Health Report
                             │
                             ▼
                         Browser
```

---

# 📈 Example Prediction Lifecycle

Given a patient submits:

```text
Age              → 55
Sex              → 1
Chest Pain       → 3
Resting BP       → 140
Cholesterol      → 250
Fasting Sugar    → 0
Resting ECG      → 1
Max Heart Rate   → 140
Exercise Angina  → 1
ST Depression    → 2.3
Slope            → 1
Major Vessels    → 1
Thal             → 3
```

CardioSense performs:

```text
1. Validate inputs
        ↓
2. Sanitize values
        ↓
3. Create feature vector
        ↓
4. Run selected models
        ↓
5. Generate probabilities
        ↓
6. Calculate ensemble score
        ↓
7. Determine prediction
        ↓
8. Determine risk tier
        ↓
9. Identify risk factors
        ↓
10. Generate recommendations
        ↓
11. Generate detailed summary
```

---

# 🔮 Future Improvements

Potential future improvements include:

- Integration with a validated real-world clinical dataset.
- More extensive hyperparameter optimization.
- ROC-AUC, precision, recall and F1-score reporting.
- Confusion matrix visualization.
- Feature importance visualization.
- SHAP-based model explainability.
- Model calibration.
- Better probability calibration.
- User authentication.
- Patient history storage.
- Database integration.
- Downloadable PDF reports.
- More detailed analytics for bulk predictions.
- Role-based access for healthcare professionals.
- Docker containerization.
- CI/CD pipeline.
- Cloud-based model monitoring.
- Model versioning.
- Automated retraining pipelines.
- Improved clinical validation before real-world use.

---

# ⚠️ Medical Disclaimer

**CardioSense AI is an educational and academic machine learning project.**

It is **not a medical device**, diagnostic system, or substitute for professional medical advice.

The predictions generated by this application should **not** be used to:

- Diagnose heart disease.
- Start or stop medication.
- Replace a physician's evaluation.
- Make emergency medical decisions.
- Determine a patient's definitive cardiovascular risk.

The model outputs are based on machine learning patterns and application-level risk rules and may contain errors.

If you have concerning symptoms or believe you may be experiencing a medical emergency, seek immediate professional medical care.

---

# 👨‍💻 Contributors

This project was developed as a **B.Tech Final Year Project (BTP)**.

### Contributors

- **Kunal Kashyap** — @Kunal13Kashyap
- **Ayush** — @Ayush-star848

---

# 📜 License

This project is licensed under the **MIT License**.

You are free to use, modify, and distribute the project according to the terms of the license.

---

# ❤️ Built With

Built with:

```text
Python
Flask
Scikit-learn
XGBoost
Pandas
NumPy
Joblib
HTML
CSS
JavaScript
Pytest
Gunicorn
```

---

# 🚀 CardioSense AI

**Heart Disease Prediction Using Ensemble Machine Learning**

> *Turning cardiovascular health data into understandable risk insights.*

🌐 **Live Demo:** https://cardiosense-ai-q5wf.onrender.com/

⭐ If you find this project useful, consider giving the repository a star.
CardioSense AI is a full-stack machine learning web application designed to assess the risk of heart disease using patient health parameters and multiple machine learning models.

The platform provides **single-patient prediction**, **bulk patient analysis through CSV uploads**, model-level prediction results, risk classification, and personalized health recommendations through an interactive web interface.

🌐 **Live Demo:** [CardioSense AI](https://cardiosense-ai-q5wf.onrender.com/)

---

## ✨ Features

### 🧠 Multi-Model Machine Learning

CardioSense AI uses multiple machine learning algorithms to analyze cardiovascular risk:

- Logistic Regression
- Random Forest
- Support Vector Machine (SVM)
- XGBoost
- Gradient Boosting
- K-Nearest Neighbors (KNN)
- Naïve Bayes
- Decision Tree
- Voting Ensemble

The system provides individual model predictions and combines model outputs through a **Voting Ensemble** to generate an overall risk assessment.

---

### 🩺 Single Patient Risk Assessment

Users can enter patient health parameters through the web interface, including:

- Age
- Sex
- Chest pain type
- Resting blood pressure
- Cholesterol
- Fasting blood sugar
- Resting ECG results
- Maximum heart rate
- Exercise-induced angina
- ST depression
- Slope
- Number of major vessels
- Thalassemia-related measurement

The application validates the submitted data before sending it to the prediction engine.

---

### 📊 Risk Classification

CardioSense AI classifies cardiovascular risk into three levels:

| Risk Level | Probability |
|------------|-------------|
| 🟢 **Low** | Below 40% |
| 🟡 **Medium** | 40% – 64% |
| 🔴 **High** | 65% and above |

The final risk classification is based on the ensemble prediction probability.

---

### 📁 Bulk Patient Analysis

CardioSense AI supports batch prediction through CSV file uploads.

Users can:

- Upload a CSV containing multiple patient records
- Process **10–500 patient records**
- Validate CSV structure and data
- Identify invalid rows
- Generate predictions for valid records
- View total positive and negative cases
- View low, medium, and high-risk cases
- View average prediction probability
- Analyze individual patient predictions

The bulk prediction workflow uses the **Voting Ensemble** model.

---

### 📋 Health Reports & Recommendations

After prediction, CardioSense AI generates a detailed health-oriented summary containing:

- Risk assessment
- Risk factors
- Recommended lifestyle changes
- Diet recommendations
- Exercise guidance
- Medical follow-up suggestions
- Blood pressure management guidance
- Cholesterol-related recommendations
- Sleep and stress recommendations
- Health monitoring suggestions

> ⚠️ These recommendations are intended for educational purposes and should not replace professional medical advice.

---

### 🎨 Modern Responsive Interface

The frontend provides:

- Responsive dashboard interface
- Dark / Light theme
- Interactive prediction workflow
- Model comparison
- Risk visualization
- Detailed prediction summaries
- Bulk analysis interface
- Modern and responsive UI

---

# 🏗️ Project Architecture

```text
CardioSense/
│
├── backend/
│   ├── app.py
│   │
│   ├── models/
│   │   ├── predictor.py
│   │   ├── trainer.py
│   │   └── __init__.py
│   │
│   ├── routes/
│   │   ├── pages.py
│   │   ├── predict.py
│   │   ├── bulk.py
│   │   ├── health.py
│   │   └── __init__.py
│   │
│   └── utils/
│       ├── validators.py
│       ├── recommendations.py
│       └── __init__.py
│
├── frontend/
│   ├── templates/
│   │   ├── index.html
│   │   ├── bulk.html
│   │   └── summary.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       │
│       └── js/
│           ├── app.js
│           └── bulk.js
│
├── data/
│   └── models/
│       ├── scaler.pkl
│       ├── logistic_regression.pkl
│       ├── random_forest.pkl
│       ├── svm.pkl
│       ├── xgboost.pkl
│       ├── gradient_boosting.pkl
│       ├── knn.pkl
│       ├── naive_bayes.pkl
│       ├── decision_tree.pkl
│       └── voting_ensemble.pkl
│
├── tests/
│   ├── test_routes.py
│   ├── test_validators.py
│   └── __init__.py
│
├── run.py
├── requirements.txt
└── README.md
```
---

# 🤖 Machine Learning Models

CardioSense AI uses eight individual classification algorithms along with a Voting Ensemble.

| Model | Reported Accuracy |
|-------|-------------------|
| ⭐ **Voting Ensemble** | **96%** |
| **XGBoost** | **95%** |
| **Gradient Boosting** | **94%** |
| **Random Forest** | **93%** |
| **Support Vector Machine** | **91%** |
| **Logistic Regression** | **86%** |
| **K-Nearest Neighbors** | **85%** |
| **Decision Tree** | **84%** |
| **Naïve Bayes** | **82%** |

> Accuracy values represent the model evaluation configuration used in this project and should not be interpreted as clinical diagnostic accuracy.

---

# 🔄 Prediction Workflow

```text
                    Patient Input
                         │
                         ▼
                 Input Validation
                         │
                         ▼
                 Feature Processing
                         │
                         ▼
              ┌─────────────────────┐
              │   Machine Learning  │
              │       Models        │
              └─────────────────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
       Model 1        Model 2        Model N
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                 Voting Ensemble
                         │
                         ▼
                 Risk Probability
                         │
                         ▼
             Low / Medium / High Risk
                         │
                         ▼
            Recommendations & Report
