from flask import Flask


def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.secret_key = "dev"  # override via environment in production

    from .blueprints.ui import ui_bp
    from .blueprints.api import api_bp

    app.register_blueprint(ui_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
