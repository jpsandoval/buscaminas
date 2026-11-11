from __future__ import annotations

import os

from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev")

    from .routes import bp

    app.register_blueprint(bp)

    return app
