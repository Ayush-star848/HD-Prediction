# """
# backend/routes/predict.py
# ==========================
# POST /api/predict  — single patient prediction
# """
# from flask import Blueprint, request, jsonify
# from backend.models.predictor import predictor
# from backend.utils.validators import validate_inputs
# from backend.utils.recommendations import build_recommendations, build_detail_summary

# predict_bp = Blueprint("predict", __name__)


# @predict_bp.route("/api/predict", methods=["POST"])
# def predict():
#     payload = request.get_json(silent=True)
#     if payload is None:
#         return jsonify({"success": False, "error": "Invalid JSON body"}), 400

#     v = validate_inputs(payload)
#     if not v.is_valid:
#         return jsonify({"success": False, "errors": v.errors}), 422

#     try:
#         sel = v.cleaned.pop("selected_models", None)
#         result = predictor.predict_ensemble(inputs=v.cleaned, selected_models=sel)
#     except FileNotFoundError as e:
#         return jsonify({"success": False, "error": str(e)}), 503
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500

#     recs    = build_recommendations(v.cleaned, result["risk_tier"])
#     summary = build_detail_summary(v.cleaned, result)

#     return jsonify({
#         "success":         True,
#         "model_results":   result["model_results"],
#         "ensemble_prob":   result["ensemble_prob"],
#         "ensemble_pred":   result["ensemble_pred"],
#         "risk_tier":       result["risk_tier"],
#         "positive_count":  result["positive_count"],
#         "total_models":    result["total_models"],
#         "best_model":      result["best_model"],
#         "recommendations": recs,
#         "summary":         summary,
#     }), 200


"""
backend/routes/predict.py
==========================
POST /api/predict  — single patient prediction
"""

from flask import Blueprint, request, jsonify, session
from backend.models.predictor import predictor
from backend.utils.validators import validate_inputs
from backend.utils.recommendations import (
    build_recommendations,
    build_detail_summary
)

predict_bp = Blueprint("predict", __name__)


@predict_bp.route("/api/predict", methods=["POST"])
def predict():

    payload = request.get_json(silent=True)

    if payload is None:
        return jsonify({
            "success": False,
            "error": "Invalid JSON body"
        }), 400

    v = validate_inputs(payload)

    if not v.is_valid:
        return jsonify({
            "success": False,
            "errors": v.errors
        }), 422

    try:
        sel = v.cleaned.pop("selected_models", None)

        result = predictor.predict_ensemble(
            inputs=v.cleaned,
            selected_models=sel
        )

    except FileNotFoundError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 503

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    recs = build_recommendations(
        v.cleaned,
        result["risk_tier"]
    )

    summary = build_detail_summary(
        v.cleaned,
        result
    )

    return jsonify({
        "success":         True,
        "model_results":   result["model_results"],
        "ensemble_prob":   result["ensemble_prob"],
        "ensemble_pred":   result["ensemble_pred"],
        "risk_tier":       result["risk_tier"],
        "positive_count":  result["positive_count"],
        "total_models":    result["total_models"],
        "best_model":      result["best_model"],
        "recommendations": recs,
        "summary":         summary,
    }), 200


@predict_bp.route("/api/store-summary", methods=["POST"])
def store_summary():

    try:
        summary_data = request.get_json(silent=True)

        if not summary_data:
            return jsonify({
                "success": False,
                "error": "No summary data received"
            }), 400

        # Save summary into Flask session
        session["summary_data"] = summary_data

        return jsonify({
            "success": True
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500