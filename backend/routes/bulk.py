"""
backend/routes/bulk.py
=======================
POST /api/bulk  — upload CSV of 100-200 patients, get batch predictions
"""
import io
import pandas as pd
from flask import Blueprint, request, jsonify
from backend.models.predictor import predictor
from backend.utils.validators import RULES

bulk_bp = Blueprint("bulk", __name__)

REQUIRED_COLS = list(RULES.keys())


@bulk_bp.route("/api/bulk", methods=["POST"])
def bulk_predict():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded. Send a CSV as 'file'."}), 400

    f = request.files["file"]
    if not f.filename.endswith(".csv"):
        return jsonify({"success": False, "error": "Only .csv files are accepted."}), 400

    try:
        df = pd.read_csv(io.StringIO(f.stream.read().decode("utf-8")))
    except Exception as e:
        return jsonify({"success": False, "error": f"Could not parse CSV: {e}"}), 400

    # Normalise column names
    df.columns = [c.strip().lower() for c in df.columns]

    missing_cols = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing_cols:
        return jsonify({
            "success": False,
            "error": f"CSV is missing required columns: {missing_cols}",
            "required_columns": REQUIRED_COLS,
        }), 422

    if not (10 <= len(df) <= 500):
        return jsonify({
            "success": False,
            "error": f"CSV must contain 10–500 rows (got {len(df)}).",
        }), 422

    # Build records
    records = []
    for _, row in df[REQUIRED_COLS].iterrows():
        try:
            records.append({c: float(row[c]) for c in REQUIRED_COLS})
        except Exception:
            records.append(None)

    valid_records   = [r for r in records if r is not None]
    invalid_indices = [i + 1 for i, r in enumerate(records) if r is None]

    try:
        results = predictor.batch_predict(valid_records)
    except FileNotFoundError as e:
        return jsonify({"success": False, "error": str(e)}), 503
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

    # Stats summary
    total    = len(results)
    positive = sum(1 for r in results if r.get("prediction") == 1)
    high_r   = sum(1 for r in results if r.get("risk_tier") == "high")
    med_r    = sum(1 for r in results if r.get("risk_tier") == "medium")
    low_r    = sum(1 for r in results if r.get("risk_tier") == "low")
    avg_prob = round(sum(r.get("probability", 0) for r in results) / total, 1) if total else 0

    return jsonify({
        "success":          True,
        "total_patients":   total,
        "positive_cases":   positive,
        "negative_cases":   total - positive,
        "high_risk":        high_r,
        "medium_risk":      med_r,
        "low_risk":         low_r,
        "avg_probability":  avg_prob,
        "invalid_rows":     invalid_indices,
        "model_used":       "Voting Ensemble (96% accuracy)",
        "results":          results,
    }), 200
