from flask import Flask
from flask_login import LoginManager

from .blueprints.api import api_bp
from .blueprints.auth import auth_bp
from .blueprints.main import main_bp
from .config import Config
from .services.auth_store import get_user_by_id, init_auth_db
from .extensions import db, migrate


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "main.admin_login"

    @login_manager.user_loader
    def load_user(user_id: str):
        return get_user_by_id(app, user_id)

    init_auth_db(app)
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    return app
