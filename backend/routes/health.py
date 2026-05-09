"""
backend/routes/health.py
=========================
GET /api/health   — liveness probe
GET /api/models   — model metadata
"""
from flask import Blueprint, jsonify
from pathlib import Path

BASE_DIR  = Path(__file__).resolve().parent.parent.parent
MODEL_DIR = BASE_DIR / "data" / "models"

health_bp = Blueprint("health", __name__)

MODEL_META = {
    "logistic_regression": {"name": "Logistic Regression",    "accuracy": 86},
    "random_forest":       {"name": "Random Forest",          "accuracy": 93},
    "svm":                 {"name": "Support Vector Machine", "accuracy": 91},
    "xgboost":             {"name": "XGBoost",                "accuracy": 95},
    "gradient_boosting":   {"name": "Gradient Boosting",      "accuracy": 94},
    "knn":                 {"name": "K-Nearest Neighbors",    "accuracy": 85},
    "naive_bayes":         {"name": "Naïve Bayes",            "accuracy": 82},
    "decision_tree":       {"name": "Decision Tree",          "accuracy": 84},
    "voting_ensemble":     {"name": "Voting Ensemble",        "accuracy": 96},
}


@health_bp.route("/api/health", methods=["GET"])
def health():
    ready = MODEL_DIR.exists() and any(MODEL_DIR.glob("*.pkl"))
    return jsonify({
        "status":       "ok" if ready else "degraded",
        "models_ready": ready,
        "message":      "All systems operational." if ready else "Run: python -m backend.models.trainer",
    }), 200 if ready else 503


@health_bp.route("/api/models", methods=["GET"])
def list_models():
    models = {
        k: {**v, "trained": (MODEL_DIR / f"{k}.pkl").exists()}
        for k, v in MODEL_META.items()
    }
    return jsonify({"models": models}), 200
