from datetime import datetime

from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from flask_wtf.csrf import generate_csrf
from loguru import logger

from services import auth_service

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/", methods=["GET"])
def base():
    auth_form = auth_service.get_auth_form()
    return render_template("auth.html", auth_form=auth_form)


@auth_bp.route("/sign-in", methods=["POST"])
def sign_in():
    auth_form = auth_service.get_auth_form()
    logger.debug(f"{auth_form.data = }")
    if auth_form.validate_on_submit():
        email = auth_form.email.data
        password = auth_form.password.data

        user = auth_service.sign_in_user(email, password)
        logger.debug(f"User is signed in: {user = }")
        if not user:
            logger.error("User does not exist or password is incorrect")
            auth_form.email.errors = ["Email does not exist"]
            auth_form.password.errors = ["Password not correct"]
            logger.debug(f"{auth_form.errors = }")
            return render_template("auth_form.html", auth_form=auth_form), 422

        # next_page = request.form.get("next")
        # if next_page:
        #     logger.debug(f"Redirecting to {next_page = }")
        #     return redirect(next_page)
        # else:
        #     return redirect(url_for("index_bp.get"))
        return redirect(url_for("index_bp.get"))
    else:
        logger.error(f"Sign-in form did not validate: {auth_form.errors}")
        return render_template("auth_form.html", auth_form=auth_form), 422


@auth_bp.route("/authenticated", methods=["GET"])
def authenticated():
    logger.debug(f"{current_user = } {current_user.is_authenticated = }")
    return jsonify({"authenticated": current_user.is_authenticated})


@auth_bp.route("/refresh-csrf-token", methods=["GET"])
def refresh_csrf_token():
    new_token = generate_csrf()
    logger.debug(f"{new_token = }")
    return jsonify({"token": new_token})


@auth_bp.route("/sign-out", methods=["GET"])
@login_required
def sign_out():
    auth_service.sign_out_user()
    return redirect(url_for("auth_bp.base"))
