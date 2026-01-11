from flask import Flask

from .blueprints.api import api_bp
from .blueprints.auth import auth_bp
from .blueprints.main import main_bp
from .config import Config
from .extensions import db


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()

    return app
