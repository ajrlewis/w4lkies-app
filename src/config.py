from datetime import timedelta
import os
import secrets

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # JSON settings
    JSON_SORT_KEYS = False

    # Email settings
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 465))  # default to 465 for SSL
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER_NAME = os.getenv("MAIL_DEFAULT_SENDER_NAME")
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # Session settings
    REMEMBER_COOKIE_DURATION = timedelta(
        seconds=int(os.getenv("REMEMBER_COOKIE_DURATION", 600))
    )
    PERMANENT_SESSION_LIFETIME = REMEMBER_COOKIE_DURATION

    # Security settings
    SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_urlsafe(32)
    logger.debug(f"{SECRET_KEY = }")
