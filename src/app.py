import datetime
import os
import sys

from flask import Flask, request
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from loguru import logger

from middleware.htmx import handle_htmx_redirect, refresh_csrf_token_in_response

# Configure logging
LOGURU_LEVEL = os.getenv("LOGURU_LEVEL", "INFO")
LOGURU_LEVEL = LOGURU_LEVEL.upper()
logger.remove()
logger.add(sys.stderr, level=LOGURU_LEVEL)
logger.info(f"{LOGURU_LEVEL = }")

csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()


# Create application
def create_app(Config) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    # Configure application
    app.config.from_object(Config)

    csrf.init_app(app=app)
    db.init_app(app=app)
    migrate.init_app(app, db)
    login_manager.init_app(app=app)
    mail.state = mail.init_app(app=app)

    with app.app_context():
        # Import all models for database initialization and migrations.
        import models
        from services import database_service

        # Register application routes.
        from blueprints.index_bp import index_bp
        from blueprints.auth_bp import auth_bp
        from blueprints.users_bp import users_bp
        from blueprints.customers_bp import customers_bp
        from blueprints.vets_bp import vets_bp
        from blueprints.dogs_bp import dogs_bp
        from blueprints.services_bp import services_bp
        from blueprints.bookings_bp import bookings_bp
        from blueprints.invoices_bp import invoices_bp
        from blueprints.expenses_bp import expenses_bp

        # from blueprints.income_statement_bp import income_statement_bp

        app.register_blueprint(index_bp, url_prefix="/")
        app.register_blueprint(auth_bp, url_prefix="/auth")
        app.register_blueprint(users_bp, url_prefix="/users")
        app.register_blueprint(customers_bp, url_prefix="/customers")
        app.register_blueprint(vets_bp, url_prefix="/vets")
        app.register_blueprint(dogs_bp, url_prefix="/dogs")
        app.register_blueprint(services_bp, url_prefix="/services")
        app.register_blueprint(bookings_bp, url_prefix="/bookings")
        app.register_blueprint(invoices_bp, url_prefix="/invoices")
        app.register_blueprint(expenses_bp, url_prefix="/expenses")
        # app.register_blueprint(income_statement_bp, url_prefix="/income_statement")

        # Context Handling
        @app.context_processor
        def handle_context():
            return {"current_date": datetime.datetime.utcnow().date()}

        # Request Handling
        @app.before_request
        def before_request_func():
            if request.blueprint not in [None, "auth_bp", "index_bp"]:
                logger.debug("Waking up database")
                database_service.wake_up_database()

        @app.after_request
        def after_request_func(response):
            response = handle_htmx_redirect(response)
            return response

        # Error Handling
        @app.errorhandler(404)
        def page_not_found(e):
            return "Page not found", 404

        @app.errorhandler(500)
        def internal_server_error(e):
            return "Internal server error", 500

        return app
