import os
import sys

from loguru import logger
from flask import Flask

# Configure logging
LOGURU_LEVEL = os.getenv("LOGURU_LEVEL", "INFO")
LOGURU_LEVEL = LOGURU_LEVEL.upper()
logger.remove()
logger.add(sys.stderr, level=LOGURU_LEVEL)
logger.info(f"{LOGURU_LEVEL = }")


# Create application
def create_app(Config) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    # Configure application
    app.config.from_object(Config)

    with app.app_context():
        from blueprints.index_bp import index_bp

        app.register_blueprint(index_bp, url_prefix="/")

        return app
