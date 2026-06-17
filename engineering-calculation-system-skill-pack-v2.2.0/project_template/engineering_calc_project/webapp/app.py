"""Application factory and local entrypoint for the engineering calculation web app."""

from __future__ import annotations

import sys

from flask import Flask, jsonify

from . import config as cfg

if str(cfg.SRC_DIR) not in sys.path:
    sys.path.insert(0, str(cfg.SRC_DIR))

from .routes import bp


def create_app() -> Flask:
    """Create the Flask application used by local runs and gunicorn."""
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = cfg.SECRET_KEY
    app.config["DEBUG"] = cfg.DEBUG
    app.register_blueprint(bp)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    return app


def main() -> None:
    app = create_app()
    app.run(host=cfg.HOST, port=cfg.PORT, debug=cfg.DEBUG)


if __name__ == "__main__":
    main()
