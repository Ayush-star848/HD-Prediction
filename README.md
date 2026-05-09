# CardioSense AI v2 — Heart Disease Prediction App

Full-stack Python web application with:
- 🌗 **Dark / Light theme toggler**
- ⚡ **9 ML models** including Voting Ensemble (96% accuracy)
- 📂 **Bulk CSV upload** for 10–500 patients
- 📋 **Full detail summary page** with action plan, avoid list, follow-up timeline
- 🎨 **Redesigned UI** — Syne + Instrument Serif + JetBrains Mono

---

## Project Structure

```
heart_disease_v2/
├── run.py
├── requirements.txt
│
├── backend/
│   ├── app.py                    Flask app factory
│   ├── models/
│   │   ├── trainer.py            Train 9 ML models
│   │   └── predictor.py          Inference engine
│   ├── routes/
│   │   ├── pages.py              GET / /bulk /summary
│   │   ├── predict.py            POST /api/predict
│   │   ├── bulk.py               POST /api/bulk
│   │   └── health.py             GET /api/health /api/models
│   └── utils/
│       ├── validators.py
│       └── recommendations.py    Recommendations + detail summary
│
├── frontend/
│   ├── templates/
│   │   ├── index.html            Main prediction page
│   │   ├── bulk.html             CSV bulk upload page
│   │   └── summary.html          Detail action plan page
│   └── static/
│       ├── css/style.css         Full themed stylesheet
│       └── js/
│           ├── app.js            Theme toggle + prediction logic
│           └── bulk.js           Bulk upload, table, export
│
└── tests/
```

---

## ML Models (9 total)

| Model               | Accuracy |
|---------------------|----------|
| ★ Voting Ensemble   | **96%**  |
| XGBoost             | 95%      |
| Gradient Boosting   | 94%      |
| Random Forest       | 93%      |
| SVM                 | 91%      |
| Logistic Regression | 86%      |
| K-Nearest Neighbors | 85%      |
| Decision Tree       | 84%      |
| Naïve Bayes         | 82%      |

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Train all 9 ML models
python -m backend.models.trainer

# Run the app
python run.py
# → http://localhost:5000
```

---

## Routes

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Main prediction form |
| GET | `/bulk` | Bulk CSV upload page |
| GET | `/summary?data=...` | Full patient action plan |
| POST | `/api/predict` | Single patient prediction |
| POST | `/api/bulk` | Batch CSV prediction |
| GET | `/api/health` | Liveness check |
| GET | `/api/models` | Model metadata |

---

## Bulk CSV Format

Required columns:
`age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal`

Download a sample template from the Bulk Upload page.

---

## Tests

```bash
python -m pytest tests/ -v
```
