❤️ CardioSense AI v2

AI-powered Heart Disease Prediction platform built using Flask, Machine Learning, and modern frontend architecture.
Designed for both single-patient diagnosis and bulk clinical screening with actionable health recommendations and detailed follow-up plans.

🚀 Features
⚡ Predict heart disease risk using 9 Machine Learning models
🧠 Includes a high-accuracy Voting Ensemble model (96%)
📂 Bulk CSV upload support for 10–500 patients
📋 Detailed patient summary with:
Risk analysis
Action plan
Lifestyle recommendations
Avoid list
Follow-up timeline
🌗 Dark / Light theme toggle
📊 Real-time prediction results
📥 CSV export support
🧪 REST API architecture with health monitoring routes
🎨 Modern responsive UI using:
Syne
Instrument Serif
JetBrains Mono
🛠 Tech Stack
Backend
Python
Flask
Scikit-learn
XGBoost
Pandas
NumPy
Frontend
HTML
CSS
JavaScript
Machine Learning
Voting Ensemble
XGBoost
Gradient Boosting
Random Forest
SVM
Logistic Regression
KNN
Decision Tree
Naïve Bayes
📂 Project Structure
heart_disease_v2/
├── run.py
├── requirements.txt
│
├── backend/
│   ├── app.py
│   ├── models/
│   │   ├── trainer.py
│   │   └── predictor.py
│   ├── routes/
│   │   ├── pages.py
│   │   ├── predict.py
│   │   ├── bulk.py
│   │   └── health.py
│   └── utils/
│       ├── validators.py
│       └── recommendations.py
│
├── frontend/
│   ├── templates/
│   └── static/
│
└── tests/
⚡ ML Model Performance
Model	Accuracy
⭐ Voting Ensemble	96%
XGBoost	95%
Gradient Boosting	94%
Random Forest	93%
SVM	91%
Logistic Regression	86%
KNN	85%
Decision Tree	84%
Naïve Bayes	82%
📸 Core Modules
🩺 Single Patient Prediction

Predict heart disease probability using clinical parameters with instant AI-generated recommendations.

📂 Bulk CSV Prediction

Upload CSV datasets containing multiple patients and generate predictions at scale.

📋 AI Health Summary

Detailed patient analysis page with:

Risk severity
Recommended actions
Foods & habits to avoid
Follow-up suggestions
Preventive care guidance
🌗 Theme Engine

Fully responsive dark/light mode UI with persistent theme state.

🔌 API Routes
Method	Endpoint	Description
GET	/	Main prediction interface
GET	/bulk	Bulk CSV upload page
GET	/summary	Detailed patient report
POST	/api/predict	Single prediction API
POST	/api/bulk	Bulk prediction API
GET	/api/health	Health check endpoint
GET	/api/models	Model metadata
⚙️ Installation & Setup
1️⃣ Clone Repository
git clone <your-repo-url>
cd heart_disease_v2
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Train ML Models
python -m backend.models.trainer
4️⃣ Run Application
python run.py

Application runs at:

http://localhost:5000
📂 Bulk CSV Format

Required columns:

age, sex, cp, trestbps, chol, fbs, restecg,
thalach, exang, oldpeak, slope, ca, thal
🧪 Running Tests
python -m pytest tests/ -v
🎯 Resume Highlights
Built a full-stack AI healthcare platform with scalable Flask architecture
Implemented and compared 9 ML models with ensemble learning achieving 96% accuracy
Developed bulk patient prediction workflow with CSV processing and export support
Designed responsive modern UI with theme engine and detailed recommendation system
📌 Future Improvements
JWT Authentication
Doctor Dashboard
PDF Report Generation
Email Notifications
Cloud Deployment
Model Explainability (SHAP/LIME)
📄 License

This project is built for educational and portfolio purposes.
