# ❤️ CardioSense AI

### AI-Powered Heart Disease Risk Prediction & Assessment Platform

CardioSense AI is a full-stack machine learning web application that predicts heart disease risk using **multiple classification models and a soft-voting ensemble**.

The platform supports **individual patient assessment** as well as **bulk CSV-based analysis**, and provides risk classification, model-level predictions, personalized recommendations, and detailed health action plans.

> ⚠️ **Educational & Research Project:** CardioSense is not a medical diagnostic tool and should not be used as a substitute for professional medical advice.

---

## 🚀 Live Demo

🌐 **[CardioSense AI](https://web-production-9eb80.up.railway.app/)**

---

## ✨ Features

### 🤖 Machine Learning

- 8 individual machine learning classification models
- Soft-voting ensemble model
- Probability-based predictions
- Model-wise prediction comparison
- Model accuracy comparison
- Automatic model loading using `joblib`
- Feature scaling using `StandardScaler`
- Top-performing models selected for the ensemble

### 🩺 Individual Assessment

- Interactive cardiovascular health assessment form
- 13 patient input features
- Input validation and sanitization
- Selectable prediction models
- Individual model predictions
- Ensemble prediction
- Overall risk probability
- Low / Medium / High risk classification
- Best-performing model identification

### 📊 Bulk Patient Analysis

- CSV file upload
- Supports **10–500 patient records**
- Automatic column normalization
- Required-column validation
- Invalid-row detection
- Batch prediction using the Voting Ensemble
- Patient-level prediction results
- Aggregate statistics
- Average prediction probability
- Risk distribution analysis

### 📋 Health Insights

CardioSense generates a detailed health action plan containing:

- Risk factors
- Immediate actions
- Lifestyle recommendations
- Diet recommendations
- Exercise guidance
- Medical follow-up suggestions
- Things to avoid
- Warning signs
- Follow-up schedule
- Clinical discussion points

### 🎨 User Interface

- Responsive web design
- Dark / Light theme
- Interactive assessment dashboard
- Bulk analysis interface
- Detailed prediction results
- Health summary page
- Printable action plan
- Custom CSS styling
- Modern typography

### 🔌 REST API

The backend provides Flask-based API endpoints for:

- Individual predictions
- Bulk predictions
- Model metadata
- Application health checks
- Summary generation

---

# 📸 Screenshots

> Add screenshots of the application here to make the repository more visually appealing.

### 🩺 Individual Assessment

![CardioSense Assessment](screenshots/assessment.png)

### 📊 Prediction Results

![CardioSense Results](screenshots/results.png)

### 📁 Bulk Analysis

![CardioSense Bulk Analysis](screenshots/bulk.png)

### 📋 Health Action Plan

![CardioSense Health Summary](screenshots/summary.png)

> If your screenshots are stored somewhere else, update the paths above accordingly.

---

# 🧠 Machine Learning

CardioSense uses multiple classification algorithms and combines the strongest-performing models using a **soft-voting ensemble**.

## Models

| Model | Configured Accuracy |
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

> The accuracy values shown above are the model metadata configured in the application. They should not be interpreted as clinically validated performance metrics.

---

## 🏆 Ensemble Strategy

The training pipeline evaluates the individual models and uses the **top 4 performing models** to construct the soft-voting ensemble.

```text
                    Patient Features
                           │
                           ▼
                  ┌─────────────────┐
                  │ Input Validation│
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Feature Scaling │
                  └────────┬────────┘
                           │
                           ▼
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
           Model 1      Model 2      Model 3 ...
              │            │            │
              └────────────┼────────────┘
                           │
                           ▼
                 Probability Estimates
                           │
                           ▼
                  Soft Voting Ensemble
                           │
                           ▼
                    Risk Probability
                           │
                           ▼
                 Risk Classification
                           │
                           ▼
              Recommendations & Summary
```

---

# 🔬 Training Pipeline

The machine learning training pipeline is implemented in:

```text
backend/models/trainer.py
```

The training workflow consists of:

```text
Dataset Generation
        ↓
Feature / Target Separation
        ↓
Stratified Train/Test Split
        ↓
Feature Scaling
        ↓
Individual Model Training
        ↓
Test Accuracy Evaluation
        ↓
5-Fold Cross Validation
        ↓
Top 4 Model Selection
        ↓
Soft Voting Ensemble
        ↓
Model Persistence
```

Trained models are saved using `joblib` and loaded by the prediction engine during application runtime.

---

# 📚 Dataset

CardioSense currently uses a **synthetic Cleveland-mirrored dataset** generated by the training pipeline.

The default configuration generates:

```text
1,200 records
13 input features
1 binary target
```

The dataset generation process uses a fixed random seed for reproducibility:

```python
generate_data(n=1200, seed=42)
```

> Because the current dataset is synthetic, model performance should not be considered representative of real-world clinical performance.

---

# 🧾 Input Features

CardioSense uses 13 cardiovascular health features:

| Feature | Description |
|---|---|
| `age` | Patient age |
| `sex` | Sex category |
| `cp` | Chest pain type |
| `trestbps` | Resting blood pressure |
| `chol` | Serum cholesterol |
| `fbs` | Fasting blood sugar indicator |
| `restecg` | Resting ECG result |
| `thalach` | Maximum heart rate achieved |
| `exang` | Exercise-induced angina |
| `oldpeak` | ST depression |
| `slope` | ST segment slope |
| `ca` | Number of major vessels |
| `thal` | Thalassemia-related category |

---

# 🚦 Risk Classification

The application converts the ensemble probability into three application-level risk tiers:

| Probability | Risk Tier |
|---:|---|
| `< 40%` | 🟢 Low |
| `40% – 64%` | 🟡 Medium |
| `≥ 65%` | 🔴 High |

For binary disease prediction, the application uses a **50% probability threshold**:

```text
Probability >= 50%
        │
        ├── 1 → Disease Predicted
        │
        └── 0 → No Disease Predicted
```

These thresholds are application-level rules and **are not clinically validated diagnostic thresholds**.

---

# 🔮 Prediction Workflow

## Individual Prediction

```text
Patient Input
      │
      ▼
Validation & Sanitization
      │
      ▼
Feature Vector
      │
      ▼
Selected ML Models
      │
      ▼
Model Predictions
      │
      ▼
Probability Scores
      │
      ▼
Ensemble Risk Score
      │
      ▼
Risk Tier
   ┌──┼──┐
   ▼  ▼  ▼
 Low Med High
      │
      ▼
Risk Factor Detection
      │
      ▼
Personalized Recommendations
      │
      ▼
Detailed Health Summary
```

---

# 📊 Bulk Prediction Workflow

CardioSense supports batch analysis through CSV uploads.

```text
CSV Upload
    │
    ▼
File Validation
    │
    ▼
CSV Parsing
    │
    ▼
Column Normalization
    │
    ▼
Required Column Validation
    │
    ▼
Row Validation
    │
    ▼
Voting Ensemble
    │
    ▼
Patient-Level Predictions
    │
    ▼
Aggregate Statistics
```

### Upload Limits

| Limit | Value |
|---|---:|
| Minimum records | 10 |
| Maximum records | 500 |
| Maximum file size | 10 MB |

Invalid rows are identified separately so that valid records can still be processed.

---

# 📁 Bulk CSV Format

The CSV file should contain the following columns:

```text
age
sex
cp
trestbps
chol
fbs
restecg
thalach
exang
oldpeak
slope
ca
thal
```

### Example

```csv
age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal
63,1,3,145,233,1,0,150,0,2.3,0,0,1
55,1,2,140,250,0,1,140,1,2.3,1,1,3
48,0,1,120,210,0,0,170,0,0.5,1,0,2
```

Column names are normalized before validation to handle variations in capitalization and whitespace.

---

# 💡 Personalized Recommendations

The recommendation engine is implemented in:

```text
backend/utils/recommendations.py
```

It generates recommendations based on the patient's prediction and relevant input factors.

Depending on the assessment, recommendations can cover:

- 🥗 Diet
- 🏃 Physical activity
- 🩸 Blood pressure
- 🧪 Cholesterol
- 🍬 Blood sugar
- 🏥 Medical follow-up
- 🫀 Cardiovascular risk factors
- 🚭 Smoking and alcohol
- 😴 Sleep and stress
- 📅 Monitoring and follow-up

---

# 📋 Health Action Plan

The detailed summary provides a structured report containing:

### Risk Factors

Potential cardiovascular risk factors identified from the submitted information.

### Immediate Actions

Actions based on the calculated risk tier.

### What To Do

Personalized recommendations covering areas such as:

- Diet
- Exercise
- Medical care
- Lifestyle

### What To Avoid

Potentially harmful lifestyle or dietary factors identified by the recommendation engine.

### Warning Signs

Symptoms that may require appropriate medical attention.

### Follow-up Schedule

A follow-up timeline based on the application's risk classification.

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │       Browser       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Flask Backend    │
                         └──────────┬──────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
                ▼                   ▼                   ▼
          Page Routes         Prediction API        Bulk API
                │                   │                   │
                │                   ▼                   ▼
                │              Validation          CSV Parsing
                │                   │                   │
                │                   ▼                   ▼
                │            Predictor Engine      Batch Engine
                │                   │                   │
                │                   ▼                   │
                │              ML Models              │
                │                   │                   │
                │                   ▼                   ▼
                │            Ensemble Prediction
                │                   │
                │                   ▼
                │             Risk Classification
                │                   │
                │                   ▼
                │          Recommendation Engine
                │                   │
                └───────────────────┤
                                    ▼
                          Detailed Health Report
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
│   │   ├── trainer.py
│   │   └── predictor.py
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

# 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Language | Python |
| Backend | Flask, Flask-CORS |
| Machine Learning | Scikit-learn, XGBoost |
| Data Processing | Pandas, NumPy |
| Model Persistence | Joblib |
| Frontend | HTML5, CSS3, JavaScript |
| Templates | Jinja2 |
| Testing | Pytest |
| Production Server | Gunicorn |
| Deployment | Railway |

---

# ⚙️ Installation & Setup

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/cardiosense.git
cd cardiosense
```

Replace the repository URL with your actual GitHub repository URL.

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

If the trained model files need to be regenerated:

```bash
python -m backend.models.trainer
```

The generated model files will be stored inside:

```text
data/models/
```

---

## 5. Run the Application

```bash
python run.py
```

The application will be available at:

```text
http://localhost:5000
```

---

# 🧪 Testing

CardioSense includes automated tests using **Pytest**.

Run the test suite with:

```bash
python -m pytest tests/ -v
```

The tests cover areas including:

- Application health checks
- Model metadata
- Route behavior
- Invalid JSON handling
- Missing prediction fields
- Bulk endpoint validation
- Input validation
- Range validation
- Categorical validation
- Type conversion
- Model selection validation

---

# 🚀 Deployment

CardioSense is configured for production deployment using **Gunicorn**.

### Procfile

```text
web: gunicorn run:app --workers 2 --bind 0.0.0.0:$PORT
```

### Python Runtime

```text
python-3.11.9
```

The application is currently deployed on **Railway**.

🌐 **Live Application:**  
https://web-production-9eb80.up.railway.app/

---

# 🔐 Environment Variables

The application supports the following environment variable:

```text
SECRET_KEY
```

Example:

```text
SECRET_KEY=your-secure-secret-key
```

For production deployments, a secure randomly generated secret key should be used.

---

# 📈 Future Improvements

Some potential improvements for future versions include:

- Training on a validated real-world clinical dataset
- External test-set evaluation
- ROC-AUC, precision, recall and F1-score reporting
- Confusion matrix visualization
- Feature importance visualization
- SHAP-based explainability
- Probability calibration
- Model versioning
- Patient history
- Database integration
- User authentication
- Downloadable PDF health reports
- Advanced bulk analytics
- Docker containerization
- CI/CD integration
- Model monitoring
- Automated model retraining
- Clinical validation before real-world medical use

---

# ⚠️ Medical Disclaimer

CardioSense AI is an **educational and research-oriented machine learning project**.

It is **not a medical device, diagnostic system, or substitute for professional medical advice**.

The predictions generated by this application should not be used to:

- Diagnose heart disease
- Start or stop medication
- Replace a physician's assessment
- Make emergency medical decisions
- Determine definitive cardiovascular risk

The current model is trained using a synthetic dataset, and its predictions may not generalize to real-world patient populations.

If you have concerning symptoms or believe you may be experiencing a medical emergency, seek appropriate professional medical care immediately.

---

# 👥 Contributors

- **Ayush Gupta** — [@Ayush-star848](https://github.com/Ayush-star848)
- **Kunal Kashyap** — [@Kunal13Kashyap](https://github.com/Kunal13Kashyap)

---

# 📄 License

This project is licensed under the **MIT License**.

---

## ❤️ CardioSense AI

**Turning cardiovascular health data into understandable risk insights using Machine Learning.**

Built with:

```text
Python • Flask • Scikit-learn • XGBoost • Pandas
NumPy • HTML • CSS • JavaScript • Pytest • Gunicorn
```

⭐ **If you find CardioSense interesting, consider giving the repository a star.**
