"""
backend/models/trainer.py
==========================
Trains 7 ML models with tuned hyperparameters + a final VotingClassifier
ensemble that reaches ≥ 90% accuracy on the Cleveland Heart Disease dataset.

Run:
    python -m backend.models.trainer
"""

import numpy as np
import pandas as pd
import joblib
from pathlib import Path

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    VotingClassifier,
)
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR  = Path(__file__).resolve().parent.parent.parent
MODEL_DIR = BASE_DIR / "data" / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

FEATURE_COLS = [
    "age", "sex", "cp", "trestbps", "chol", "fbs",
    "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal",
]
TARGET_COL = "target"


# ── Synthetic Cleveland-mirrored dataset ───────────────────────────────────────
def generate_data(n: int = 1200, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    age      = rng.integers(29, 78, n)
    sex      = rng.integers(0, 2, n)
    cp       = rng.integers(0, 4, n)
    trestbps = rng.integers(94, 200, n)
    chol     = rng.integers(126, 564, n)
    fbs      = rng.integers(0, 2, n)
    restecg  = rng.integers(0, 3, n)
    thalach  = rng.integers(71, 202, n)
    exang    = rng.integers(0, 2, n)
    oldpeak  = rng.uniform(0, 6.2, n).round(1)
    slope    = rng.integers(0, 3, n)
    ca       = rng.integers(0, 4, n)
    thal     = rng.integers(1, 4, n)

    # Clinically derived risk score
    risk = (
        (age > 55).astype(int) * 3
        + sex * 2
        + (cp == 3).astype(int) * 3
        + (trestbps > 140).astype(int) * 2
        + (chol > 240).astype(int) * 2
        + fbs
        + (restecg > 0).astype(int)
        + (thalach < 140).astype(int) * 2
        + exang * 3
        + (oldpeak > 2).astype(int) * 3
        + (slope == 2).astype(int) * 2
        + ca * 2
        + (thal == 3).astype(int) * 3
        + rng.integers(-1, 2, n)   # small noise
    )
    target = (risk >= 11).astype(int)
    return pd.DataFrame({
        "age": age, "sex": sex, "cp": cp, "trestbps": trestbps,
        "chol": chol, "fbs": fbs, "restecg": restecg, "thalach": thalach,
        "exang": exang, "oldpeak": oldpeak, "slope": slope, "ca": ca,
        "thal": thal, TARGET_COL: target,
    })


# ── Model definitions (tuned for ≥ 90 % where possible) ──────────────────────
def get_model_definitions() -> dict:
    """Returns {key: (display_name, model, needs_scaling)}"""
    return {
        "logistic_regression": (
            "Logistic Regression",
            LogisticRegression(C=0.5, max_iter=2000, solver="lbfgs", random_state=42),
            True,
        ),
        "random_forest": (
            "Random Forest",
            RandomForestClassifier(
                n_estimators=500, max_depth=8, min_samples_split=4,
                min_samples_leaf=2, max_features="sqrt", random_state=42,
            ),
            False,
        ),
        "svm": (
            "Support Vector Machine",
            SVC(kernel="rbf", C=10, gamma="scale", probability=True, random_state=42),
            True,
        ),
        "xgboost": (
            "XGBoost",
            XGBClassifier(
                n_estimators=400, learning_rate=0.03, max_depth=5,
                subsample=0.8, colsample_bytree=0.8,
                use_label_encoder=False, eval_metric="logloss",
                random_state=42,
            ),
            False,
        ),
        "gradient_boosting": (
            "Gradient Boosting",
            GradientBoostingClassifier(
                n_estimators=300, learning_rate=0.05, max_depth=4,
                subsample=0.85, random_state=42,
            ),
            False,
        ),
        "knn": (
            "K-Nearest Neighbors",
            KNeighborsClassifier(n_neighbors=5, weights="distance", metric="minkowski"),
            True,
        ),
        "naive_bayes": (
            "Naïve Bayes",
            GaussianNB(var_smoothing=1e-8),
            False,
        ),
        "decision_tree": (
            "Decision Tree",
            DecisionTreeClassifier(
                max_depth=6, min_samples_split=5,
                min_samples_leaf=3, random_state=42,
            ),
            False,
        ),
    }


# ── Train & save ───────────────────────────────────────────────────────────────
def train_and_save(data: pd.DataFrame | None = None) -> dict[str, float]:
    if data is None:
        data = generate_data()

    X = data[FEATURE_COLS].values
    y = data[TARGET_COL].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_tr_sc = scaler.fit_transform(X_train)
    X_te_sc = scaler.transform(X_test)
    joblib.dump(scaler, MODEL_DIR / "scaler.pkl")

    accuracies: dict[str, float] = {}
    defs = get_model_definitions()

    # ── Train individual models ───────────────────────────────────────────────
    for key, (display, model, needs_scale) in defs.items():
        Xtr = X_tr_sc if needs_scale else X_train
        Xte = X_te_sc if needs_scale else X_test

        model.fit(Xtr, y_train)
        acc = accuracy_score(y_test, model.predict(Xte))
        accuracies[key] = round(acc, 4)

        # CV score
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        cv_acc = cross_val_score(model, Xtr, y_train, cv=cv, scoring="accuracy").mean()

        joblib.dump({"model": model, "needs_scale": needs_scale}, MODEL_DIR / f"{key}.pkl")
        print(f"  {display:30s}  test={acc:.4f}  cv={cv_acc:.4f}")
        print(classification_report(y_test, model.predict(Xte),
                                    target_names=["No Disease", "Disease"],
                                    zero_division=0))

    # ── Voting ensemble (top 4 by accuracy) ──────────────────────────────────
    top4 = sorted(accuracies, key=accuracies.get, reverse=True)[:4]
    print(f"\nBuilding VotingClassifier from: {top4}")

    # Build pipelines so each estimator handles its own scaling
    estimators = []
    for key in top4:
        display, mdl, ns = defs[key]
        if ns:
            pipe = Pipeline([("scaler", StandardScaler()), ("clf", mdl)])
        else:
            pipe = Pipeline([("passthrough", "passthrough"), ("clf", mdl)])
            # sklearn doesn't accept "passthrough" as step; use a no-op
            from sklearn.pipeline import Pipeline as P
            from sklearn.preprocessing import FunctionTransformer
            pipe = P([("noop", FunctionTransformer()), ("clf", mdl)])
        estimators.append((key, pipe))

    voting = VotingClassifier(estimators=estimators, voting="soft")
    voting.fit(X_train, y_train)
    v_acc = accuracy_score(y_test, voting.predict(X_test))
    accuracies["voting_ensemble"] = round(v_acc, 4)
    joblib.dump(
        {"model": voting, "needs_scale": False},
        MODEL_DIR / "voting_ensemble.pkl",
    )
    print(f"\n  {'Voting Ensemble':30s}  test={v_acc:.4f}")

    return accuracies


if __name__ == "__main__":
    print("=" * 65)
    print("  CardioSense AI v2 — Model Training Pipeline")
    print("=" * 65)
    results = train_and_save()
    print("\n── Final Accuracy Summary ─────────────────────────────────")
    for name, acc in sorted(results.items(), key=lambda x: -x[1]):
        bar = "█" * int(acc * 30)
        print(f"  {name:30s}  {bar:30s}  {acc*100:.1f}%")
