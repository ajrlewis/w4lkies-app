import datetime

from flask import Blueprint, render_template, Response, request, send_from_directory
from flask_login import current_user, login_required
from loguru import logger

from services import service_service


services_bp = Blueprint("services_bp", __name__)


@services_bp.route("/base", methods=["GET"])
@login_required
def get_services_base():
    return render_template("services/services_base.html")


@services_bp.route("/info", methods=["GET"])
@login_required
def get_services_info():
    services = service_service.get_services()
    logger.debug(f"{services = }")
    return render_template("services/services_info.html", services=services)


@services_bp.route("/", methods=["GET"])
@login_required
def get_services():
    data = request.args.to_dict(flat=True)
    logger.debug(f"{data = }")
    services = service_service.get_services(**data)
    logger.debug(f"{services = }")
    return render_template("services/services.html", services=services)


@services_bp.route("/<int:service_id>", methods=["GET"])
@login_required
def get_service_by_id(service_id: int):
    service = service_service.get_service_by_id(service_id)
    logger.debug(f"{service = }")
    if service:
        return render_template("services/service_detail.html", service=service)
    return "", 404


@services_bp.route("/add", methods=["GET"])
@login_required
def get_service_form():
    service_form = service_service.get_service_form()
    logger.debug(f"{service_form = }")
    return render_template("services/service_form.html", service_form=service_form)


@services_bp.route("/<int:service_id>/edit", methods=["GET"])
@login_required
def edit_service(service_id: int):
    logger.debug(f"{service_id = }")
    service = service_service.get_service_by_id(service_id)
    logger.debug(f"{service = }")
    service_form = service_service.get_service_form(service)
    logger.debug(f"{service_form = }")
    return render_template(
        "services/service_edit.html", service=service, service_form=service_form
    )


@services_bp.route("/<int:service_id>", methods=["PUT"])
@login_required
def update_service(service_id: int):
    logger.debug(f"{service_id = }")
    service = service_service.get_service_by_id(service_id)
    service_form = service_service.get_service_form()
    logger.debug(f"{service_form = }")
    if service_form.validate_on_submit():
        service_data = service_form.data
        service_data = service_data | {
            "updated_by": current_user.user_id,
            "updated_at": datetime.datetime.utcnow(),
        }
        logger.debug(f"{service_data = }")
        service = service_service.update_service_by_id(service_id, service_data)
        return render_template("services/service_detail.html", service=service)
    else:
        logger.error(f"{service_form.errors = }")
        return (
            render_template(
                "services/service_edit.html",
                service=service,
                service_form=service_form,
            ),
            422,
        )


@services_bp.route("/", methods=["POST"])
@login_required
def add_service():
    # Add new service
    service_form = service_service.get_service_form()
    if service_form.validate_on_submit():
        service_data = service_form.data
        service_data = service_data | {"created_by": current_user.user_id}
        logger.debug(f"{service_data = }")
        service = service_service.add_service(service_data=service_data)
        logger.debug(f"{service = }")
    else:
        logger.error(f"{service_form.errors = }")
        return (
            render_template("services/service_form.html", service_form=service_form),
            422,
        )
    # Reset form
    service_form = service_service.get_service_form(ignore_request_data=True)
    logger.debug(f"{service_form = }")
    logger.debug(f"{service_form.data = }")
    return render_template("services/service_form.html", service_form=service_form)


@services_bp.route("/<int:service_id>", methods=["DELETE"])
@login_required
def delete_service_by_id(service_id: int):
    logger.debug(f"{service_id = }")
    service_service.delete_service_by_id(service_id)
    return ""
