import os
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_redis import FlaskRedis
from flask_login import LoginManager
from flask_admin import Admin

# Globally accessible libraries
db = SQLAlchemy()
login_manager = LoginManager()
admin_flask = Admin(name="jspanda_business", url="/db_admin")

from .main import main_routes
from .admin import admin_routes
from .auth import auth_routes
from .ssl_validation import ssl_validation_bp


def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)

    admin_flask.init_app(app)

    with app.app_context():
        # create all tables
        db.create_all()

        from .jspanda_orders import jspanda_orders_routes
        from .users_admin import users_admin_routes
        from .db_admin import db_admin_bp

        app.config['JSPANDA_STATS_FOLDER'] = os.path.join(app.root_path, 'static', 'img')

        # Register Blueprints
        app.register_blueprint(main_routes.main_bp)
        app.register_blueprint(admin_routes.admin_bp)
        app.register_blueprint(auth_routes.auth_bp)
        app.register_blueprint(jspanda_orders_routes.jspanda_orders_bp)
        app.register_blueprint(users_admin_routes.users_admin_bp)
        app.register_blueprint(ssl_validation_bp)
        app.register_blueprint(db_admin_bp)

        return app
