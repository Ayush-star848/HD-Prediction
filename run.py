"""
CardioSense AI v2 — Entry Point
================================
Run:   python run.py
Train: python -m backend.models.trainer
"""
from backend.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
