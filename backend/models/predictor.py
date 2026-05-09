"""
backend/models/predictor.py
============================
Singleton predictor: loads all trained models once, runs ensemble inference.
"""

import joblib
import numpy as np
from pathlib import Path
from typing import Optional

BASE_DIR  = Path(__file__).resolve().parent.parent.parent
MODEL_DIR = BASE_DIR / "data" / "models"

FEATURE_COLS = [
    "age", "sex", "cp", "trestbps", "chol", "fbs",
    "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal",
]

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


class HeartDiseasePredictor:
    def __init__(self):
        self._models: dict = {}
        self._scaler = None
        self._loaded = False

    def _load(self):
        sp = MODEL_DIR / "scaler.pkl"
        if not sp.exists():
            raise FileNotFoundError(
                f"Models not found. Run: python -m backend.models.trainer"
            )
        self._scaler = joblib.load(sp)
        for key in MODEL_META:
            path = MODEL_DIR / f"{key}.pkl"
            if path.exists():
                self._models[key] = joblib.load(path)
        self._loaded = True

    def _ensure(self):
        if not self._loaded:
            self._load()

    @staticmethod
    def to_vector(inputs: dict) -> np.ndarray:
        return np.array([[float(inputs[c]) for c in FEATURE_COLS]])

    def predict_one(self, key: str, vec: np.ndarray) -> dict:
        self._ensure()
        entry = self._models[key]
        model, ns = entry["model"], entry["needs_scale"]
        X = self._scaler.transform(vec) if ns else vec
        pred = int(model.predict(X)[0])
        prob = (
            int(round(model.predict_proba(X)[0][1] * 100))
            if hasattr(model, "predict_proba") else pred * 100
        )
        return {
            "key":          key,
            "display_name": MODEL_META[key]["name"],
            "prediction":   pred,
            "probability":  prob,
            "accuracy":     MODEL_META[key]["accuracy"],
        }

    def predict_ensemble(
        self,
        inputs: dict,
        selected_models: Optional[list] = None,
    ) -> dict:
        self._ensure()
        keys = selected_models or list(self._models.keys())
        keys = [k for k in keys if k in self._models]
        if not keys:
            raise ValueError("No valid models selected.")

        vec     = self.to_vector(inputs)
        results = [self.predict_one(k, vec) for k in keys]
        probs   = [r["probability"] for r in results]
        avg     = int(round(sum(probs) / len(probs)))
        pos_cnt = sum(1 for r in results if r["prediction"] == 1)

        risk_tier = "high" if avg >= 65 else "medium" if avg >= 40 else "low"

        # Best single model by accuracy
        best = max(results, key=lambda r: MODEL_META.get(r["key"], {}).get("accuracy", 0))

        return {
            "model_results":  results,
            "ensemble_prob":  avg,
            "ensemble_pred":  1 if avg >= 50 else 0,
            "risk_tier":      risk_tier,
            "positive_count": pos_cnt,
            "total_models":   len(keys),
            "best_model":     best,
        }

    def batch_predict(self, records: list[dict]) -> list[dict]:
        """Predict for a list of patient feature dicts. Returns list of result dicts."""
        self._ensure()
        out = []
        for i, rec in enumerate(records):
            try:
                vec    = self.to_vector(rec)
                result = self.predict_one("voting_ensemble", vec)
                tier   = (
                    "high"   if result["probability"] >= 65
                    else "medium" if result["probability"] >= 40
                    else "low"
                )
                out.append({
                    "patient_id":  i + 1,
                    "inputs":      rec,
                    "prediction":  result["prediction"],
                    "probability": result["probability"],
                    "risk_tier":   tier,
                    "model_used":  "Voting Ensemble",
                    "error":       None,
                })
            except Exception as e:
                out.append({
                    "patient_id": i + 1,
                    "inputs":     rec,
                    "error":      str(e),
                })
        return out


predictor = HeartDiseasePredictor()
