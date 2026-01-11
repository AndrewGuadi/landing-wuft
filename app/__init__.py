from flask import Flask

from .blueprints.api import api_bp
from .blueprints.auth import auth_bp
from .blueprints.main import main_bp
from .config import Config


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    return app
