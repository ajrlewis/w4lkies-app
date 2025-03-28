from typing import Optional

from flask_login import login_user, logout_user
from loguru import logger
from werkzeug.security import check_password_hash

from functools import wraps

from flask import render_template
from flask_login import current_user
from loguru import logger

from app import login_manager
from forms.auth_form import AuthForm
from models.user import User
from services import user_service


login_manager.login_view = "auth_bp.base"
login_manager.login_message_category = "error"


@login_manager.user_loader
def load_user(user_id: int):
    try:
        user = user_service.get_user_by_id(int(user_id))
        return user
    except Exception as e:
        logger.error(f"Unable to load user: {e}")
        return False


def get_auth_form() -> AuthForm:
    auth_form = AuthForm()
    return auth_form


def admin_user_required(f):
    @wraps(f)
    def _admin_user_required(*args, **kwargs):
        is_admin = current_user.is_admin
        # is_admin = False
        if is_admin:
            return f(*args, **kwargs)
        else:
            code = 403
            status = "Forbidden"
            message = "The current user does not have permissions to view this page."
            logger.error(message)
            return render_template(
                "error.html", code=code, status=status, message=message
            )

    return _admin_user_required


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
