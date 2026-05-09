"""
backend/app.py — Flask application factory
"""
import os
from flask import Flask
from flask_cors import CORS


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/static",
    )
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "cardiosense-v2-2025")
    app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB upload limit
    app.config["JSON_SORT_KEYS"] = False

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from .routes.pages   import pages_bp
    from .routes.predict import predict_bp
    from .routes.bulk    import bulk_bp
    from .routes.health  import health_bp

    app.register_blueprint(pages_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(bulk_bp)
    app.register_blueprint(health_bp)

    return app
