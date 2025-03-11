from datetime import datetime

from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user, current_user
from loguru import logger
from werkzeug.security import check_password_hash

from services import auth_service


from models.user import User
from services import user_service

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/", methods=["GET"])
def base():
    auth_form = auth_service.get_auth_form()
    return render_template("auth.html", auth_form=auth_form)


@auth_bp.route("/sign-in", methods=["POST"])
def sign_in():
    sign_in_form = SignInForm()
    if sign_in_form.validate_on_submit():
        email = sign_in_form.email.data
        logger.debug(f"{email = }")
        password = sign_in_form.password.data

        user = user_service.get_user_by_email(email)
        logger.debug(f"{user = }")
        if not user:
            error_message = f"User with {email = } not found!"
            logger.error(error_message)
            flash(error_message, "error")
            return redirect(url_for("auth_bp.sign_in"))

        if not check_password_hash(user.password, password):
            error_message = f"User password incorrect!"
            logger.error(error_message)
            flash(error_message, "error")
            return redirect(url_for("auth_bp.sign_in"))

        login_user(user, remember=True)

        # Send user a warning email of sign in
        # should_send_warning_email = False
        should_send_warning_email = True
        if should_send_warning_email and email not in ("test@test", "admin@admin"):
            now = datetime.now().strftime("%H:%M %Y-%m-%d")
            user_agent = request.user_agent.string
            ip_address = request.remote_addr
            html = render_template(
                "email/sign_in_notification.html",
                user=user,
                now=now,
                user_agent=user_agent,
                ip_address=ip_address,
            )
            send(
                sender="hello@w4lkies.com",
                recipient=email,
                subject="⚠️🔒 Sign-in Notification ⚠️🔒",
                html=html,
            )
            logger.debug("Sent email warning to user of sign in.")

        # Redirect to next page.
        # TODO (ajrl) Check the request is a GET method
        next_page = request.form.get("next")
        if next_page:
            logger.debug(f"Redirecting to {next_page = }")
            return redirect(next_page)
        else:
            return redirect(url_for("dashboard_bp.get"))

    else:
        flash("Sign-in form did not validate, please try again.", "error")
        return redirect(url_for("auth_bp.sign_in"))


@auth_bp.route("/sign-out", methods=["GET"])
@login_required
def sign_out():
    logout_user()
    return redirect(url_for("auth_bp.sign_in"))
