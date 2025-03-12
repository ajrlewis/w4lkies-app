import os
import sys

from flask import Flask

# from flask_cors import CORS
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# from flask_wtf.csrf import CSRFProtect
from flask_wtf import CSRFProtect
from loguru import logger

from middleware.htmx_error import htmx_error

# Configure logging
LOGURU_LEVEL = os.getenv("LOGURU_LEVEL", "INFO")
LOGURU_LEVEL = LOGURU_LEVEL.upper()
logger.remove()
logger.add(sys.stderr, level=LOGURU_LEVEL)
logger.info(f"{LOGURU_LEVEL = }")

# cors = CORS()
# csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()


# Create application
def create_app(Config) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    # Configure application
    app.config.from_object(Config)

    # cors.init_app(app=app, resources={r"/*": {"origins": "*"}})
    # csrf.init_app(app=app)
    db.init_app(app=app)
    migrate.init_app(app, db)
    login_manager.init_app(app=app)
    mail.state = mail.init_app(app=app)

    with app.app_context():
        # Import all models for database initialization and migrations.
        import models

        # Register application routes.
        from blueprints.index_bp import index_bp
        from blueprints.auth_bp import auth_bp
        from blueprints.expenses_bp import expenses_bp

        app.register_blueprint(index_bp, url_prefix="/")
        app.register_blueprint(auth_bp, url_prefix="/auth")
        app.register_blueprint(expenses_bp, url_prefix="/expenses")

        # Request Handling
        @app.before_request
        def before_request_func():
            # Code to run before each request
            pass

        @app.after_request
        def after_request_func(response):
            # Code to modify the response
            response = htmx_error(response)
            return response

        @app.teardown_request
        def teardown_request_func(exception):
            # Code to run after the request
            pass

        # Error Handling
        @app.errorhandler(404)
        def page_not_found(e):
            return "Page not found", 404

        @app.errorhandler(500)
        def internal_server_error(e):
            return "Internal server error", 500

        return app
