from datetime import timedelta
import os

from dotenv import load_dotenv
from loguru import logger

load_dotenv()


class Config:
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("SQLALCHEMY_DATABASE_URI environment variable is not set")
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
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is not set")
