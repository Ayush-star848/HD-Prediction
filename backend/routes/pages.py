"""
backend/routes/pages.py
========================
Page routes: main form, summary detail page.
"""

import json
from flask import Blueprint, render_template, request, redirect, url_for, session

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@pages_bp.route("/bulk", methods=["GET"])
def bulk_page():
    return render_template("bulk.html")


@pages_bp.route("/summary", methods=["GET"])
def summary():
    """
    GET /summary?data=<json_encoded_summary>
    Renders the full detail summary page.
    """
    raw = request.args.get("data")
    if not raw:
        return redirect(url_for("pages.index"))
    try:
        summary_data = json.loads(raw)
    except Exception:
        return redirect(url_for("pages.index"))
    return render_template("summary.html", data=summary_data)
