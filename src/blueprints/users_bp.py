from flask import Blueprint, render_template, Response, request, send_from_directory
from flask_login import login_required
from loguru import logger

from services import user_service


users_bp = Blueprint("users_bp", __name__)


@users_bp.route("/base", methods=["GET"])
@login_required
def get_users_base():
    return render_template("users/users_base.html")


@users_bp.route("/info", methods=["GET"])
@login_required
def get_users_info():
    users = user_service.get_users()
    logger.debug(f"{users = }")
    return render_template("users/users_info.html", users=users)


@users_bp.route("/", methods=["GET"])
@login_required
def get_users():
    data = request.args.to_dict(flat=True)
    logger.debug(f"{data = }")
    users = user_service.get_users(**data)
    logger.debug(f"{users = }")
    return render_template("users/users.html", users=users)


@users_bp.route("/<int:user_id>", methods=["GET"])
@login_required
def get_user_by_id(user_id: int):
    user = user_service.get_user_by_id(user_id)
    logger.debug(f"{user = }")
    if user:
        return render_template("users/user_detail.html", user=user)
    return "", 404


@users_bp.route("/add", methods=["GET"])
@login_required
def get_user_form():
    user_form = user_service.get_user_form()
    logger.debug(f"{user_form = }")
    return render_template("users/user_form.html", user_form=user_form)


@users_bp.route("/<int:user_id>/edit", methods=["GET"])
@login_required
def edit_user(user_id: int):
    logger.debug(f"{user_id = }")
    user = user_service.get_user_by_id(user_id)
    logger.debug(f"{user = }")
    user_form = user_service.get_user_form(user)
    logger.debug(f"{user_form = }")
    return render_template("users/user_edit.html", user=user, user_form=user_form)


@users_bp.route("/<int:user_id>", methods=["PUT"])
@login_required
def update_user(user_id: int):
    logger.debug(f"{user_id = }")
    user = user_service.get_user_by_id(user_id)
    user_form = user_service.get_user_form()
    logger.debug(f"{user_form = }")
    if user_form.validate_on_submit():
        user_data = user_form.data
        logger.debug(f"{user_data = }")
        user = user_service.update_user_by_id(user_id, user_data)
        return render_template("users/user_detail.html", user=user)
    else:
        logger.error(f"{user_form.errors = }")
        return (
            render_template(
                "users/user_edit.html",
                user=user,
                user_form=user_form,
            ),
            422,
        )


@users_bp.route("/", methods=["POST"])
@login_required
def add_user():
    # Add new user
    user_form = user_service.get_user_form()
    if user_form.validate_on_submit():
        user_data = user_form.data
        # user_data = user_data | {"created_by": current_user.user_id}
        logger.debug(f"{user_data = }")
        user = user_service.add_user(user_data=user_data)
        logger.debug(f"{user = }")
    else:
        logger.error(f"{user_form.errors = }")
        return (
            render_template("users/user_form.html", user_form=user_form),
            422,
        )
    # Reset form
    user_form = user_service.get_user_form(ignore_request_data=True)
    logger.debug(f"{user_form = }")
    logger.debug(f"{user_form.data = }")
    return render_template("users/user_form.html", user_form=user_form)


@users_bp.route("/<int:user_id>", methods=["DELETE"])
@login_required
def delete_user_by_id(user_id: int):
    logger.debug(f"{user_id = }")
    user_service.delete_user_by_id(user_id)
    return ""
