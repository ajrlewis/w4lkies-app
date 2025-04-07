import datetime

from flask import Blueprint, render_template, Response, request, send_from_directory
from flask_login import current_user, login_required
from loguru import logger

from services import vet_service
from services.auth_service import admin_user_required


vets_bp = Blueprint("vets_bp", __name__)


@vets_bp.route("/base", methods=["GET"])
@login_required
def get_vets_base():
    return render_template("vets/vets_base.html")


@vets_bp.route("/info", methods=["GET"])
@login_required
def get_vets_info():
    vets = vet_service.get_vets()
    logger.debug(f"{vets = }")
    return render_template("vets/vets_info.html", vets=vets)


@vets_bp.route("/", methods=["GET"])
@login_required
def get_vets():
    data = request.args.to_dict(flat=True)
    logger.debug(f"{data = }")
    vets = vet_service.get_vets(**data)
    logger.debug(f"{vets = }")
    return render_template("vets/vets.html", vets=vets)


@vets_bp.route("/<int:vet_id>", methods=["GET"])
@login_required
def get_vet_by_id(vet_id: int):
    vet = vet_service.get_vet_by_id(vet_id)
    logger.debug(f"{vet = }")
    if vet:
        return render_template("vets/vet_detail.html", vet=vet)
    return "", 404


@vets_bp.route("/add", methods=["GET"])
@login_required
@admin_user_required
def get_vet_form():
    vet_form = vet_service.get_vet_form()
    logger.debug(f"{vet_form = }")
    return render_template("vets/vet_form.html", vet_form=vet_form)


@vets_bp.route("/<int:vet_id>/edit", methods=["GET"])
@login_required
@admin_user_required
def edit_vet(vet_id: int):
    logger.debug(f"{vet_id = }")
    vet = vet_service.get_vet_by_id(vet_id)
    logger.debug(f"{vet = }")
    vet_form = vet_service.get_vet_form(vet)
    logger.debug(f"{vet_form = }")
    return render_template("vets/vet_edit.html", vet=vet, vet_form=vet_form)


@vets_bp.route("/<int:vet_id>", methods=["PUT"])
@login_required
@admin_user_required
def update_vet(vet_id: int):
    logger.debug(f"{vet_id = }")
    vet = vet_service.get_vet_by_id(vet_id)
    vet_form = vet_service.get_vet_form()
    logger.debug(f"{vet_form = }")
    if vet_form.validate_on_submit():
        vet_data = vet_form.data
        vet_data = vet_data | {
            "updated_at": datetime.datetime.utcnow(),
            "updated_by": current_user.user_id,
        }
        logger.debug(f"{vet_data = }")
        vet = vet_service.update_vet_by_id(vet_id, vet_data)
        return render_template("vets/vet_detail.html", vet=vet)
    else:
        logger.error(f"{vet_form.errors = }")
        return (
            render_template(
                "vets/vet_edit.html",
                vet=vet,
                vet_form=vet_form,
            ),
            422,
        )


@vets_bp.route("/", methods=["POST"])
@login_required
@admin_user_required
def add_vet():
    # Add new vet
    vet_form = vet_service.get_vet_form()
    if vet_form.validate_on_submit():
        vet_data = vet_form.data
        vet_data = vet_data | {"created_by": current_user.user_id}
        logger.debug(f"{vet_data = }")
        vet = vet_service.add_vet(vet_data=vet_data)
        logger.debug(f"{vet = }")
    else:
        logger.error(f"{vet_form.errors = }")
        return (
            render_template("vets/vet_form.html", vet_form=vet_form),
            422,
        )
    # Reset form
    vet_form = vet_service.get_vet_form(ignore_request_data=True)
    logger.debug(f"{vet_form = }")
    logger.debug(f"{vet_form.data = }")
    return render_template("vets/vet_form.html", vet_form=vet_form)


@vets_bp.route("/<int:vet_id>", methods=["DELETE"])
@login_required
@admin_user_required
def delete_vet_by_id(vet_id: int):
    logger.debug(f"{vet_id = }")
    vet_service.delete_vet_by_id(vet_id)
    return ""
