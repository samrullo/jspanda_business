from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_redis import FlaskRedis
from flask_login import LoginManager

# Globally accessible libraries
db = SQLAlchemy()
login_manager = LoginManager()

from .main import main_routes
from .admin import admin_routes
from .auth import auth_routes


def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # Register Blueprints
        app.register_blueprint(main_routes.main_bp)
        app.register_blueprint(admin_routes.admin_bp)
        app.register_blueprint(auth_routes.auth_bp)

        # create all tables
        db.create_all()
        return app
