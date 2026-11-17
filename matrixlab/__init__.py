"""MatrixLab application factory; mathematics lives outside Flask."""
from flask import Flask, jsonify, render_template, request
from .api import api


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(MAX_CONTENT_LENGTH=1_000_000, JSON_SORT_KEYS=False)
    if test_config:
        app.config.update(test_config)
    app.json.ensure_ascii = False
    app.register_blueprint(api, url_prefix="/api")

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith("/api/"):
            return jsonify(error={"code": "not_found", "message": "Endpoint não encontrado."}), 404
        return render_template("404.html"), 404

    @app.after_request
    def response_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "same-origin"
        return response

    return app
