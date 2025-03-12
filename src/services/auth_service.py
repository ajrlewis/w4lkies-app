from typing import Optional

from flask_login import login_user, logout_user
from loguru import logger
from werkzeug.security import check_password_hash

from app import login_manager
from forms.auth_form import AuthForm
from models.user import User
from services import user_service

login_manager.login_view = "auth_bp.base"
login_manager.login_message_category = "error"


@login_manager.user_loader
def load_user(user_id: int):
    user = user_service.get_user_by_id(int(user_id))
    return user


def get_auth_form() -> AuthForm:
    auth_form = AuthForm()
    return auth_form


def sign_in_user(email: str, password: str) -> Optional[User]:
    user = user_service.get_user_by_email(email)
    logger.debug(f"{user = }")
    if not user:
        logger.error(f"User with {email = } not found!")
        return
    if not check_password_hash(user.password_hash, password):
        logger.error(f"User password incorrect!")
        return
    login_user(user, remember=True)
    return user


def sign_out_user():
    logout_user()
