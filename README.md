# ❤️ CardioSense AI

### AI-Powered Heart Disease Risk Prediction & Analysis Platform

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
