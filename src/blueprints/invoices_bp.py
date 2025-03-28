from flask import (
    Blueprint,
    render_template,
    Response,
    request,
    send_file,
    send_from_directory,
)
from flask_login import login_required
from loguru import logger

from services import invoice_service
from services.auth_service import admin_user_required

invoices_bp = Blueprint("invoices_bp", __name__)


@invoices_bp.route("/base", methods=["GET"])
@login_required
@admin_user_required
def get_invoices_base():
    return render_template("invoices/invoices_base.html")


@invoices_bp.route("/info", methods=["GET"])
@login_required
@admin_user_required
def get_invoices_info():
    invoices = invoice_service.get_invoices()
    invoice_generate_form = invoice_service.get_invoice_generate_form()
    logger.debug(f"{invoices = }")
    return render_template(
        "invoices/invoices_info.html",
        invoices=invoices,
        invoice_generate_form=invoice_generate_form,
    )


@invoices_bp.route("/", methods=["GET"])
@login_required
@admin_user_required
def get_invoices():
    data = request.args.to_dict(flat=True)
    logger.debug(f"{data = }")
    invoices = invoice_service.get_invoices(**data)
    logger.debug(f"{invoices = }")
    return render_template("invoices/invoices.html", invoices=invoices)


@invoices_bp.route("/<int:invoice_id>", methods=["GET"])
@login_required
@admin_user_required
def get_invoice_by_id(invoice_id: int):
    invoice = invoice_service.get_invoice_by_id(invoice_id)
    logger.debug(f"{invoice = }")
    if invoice:
        return render_template("invoices/invoice_detail.html", invoice=invoice)
    return "", 404


@invoices_bp.route("/generate", methods=["GET"])
@login_required
@admin_user_required
def get_invoice_form():
    invoice_generate_form = invoice_service.get_invoice_generate_form()
    logger.debug(f"{invoice_generate_form = }")
    return render_template(
        "invoices/invoice_generate_form.html",
        invoice_generate_form=invoice_generate_form,
    )


@invoices_bp.route("/<int:invoice_id>/edit", methods=["GET"])
@login_required
@admin_user_required
def edit_invoice(invoice_id: int):
    logger.debug(f"{invoice_id = }")
    invoice = invoice_service.get_invoice_by_id(invoice_id)
    logger.debug(f"{invoice = }")
    invoice_form = invoice_service.get_invoice_form(invoice)
    logger.debug(f"{invoice_form = }")
    return render_template(
        "invoices/invoice_edit.html", invoice=invoice, invoice_form=invoice_form
    )


@invoices_bp.route("/<int:invoice_id>", methods=["PUT"])
@login_required
@admin_user_required
def update_invoice(invoice_id: int):
    logger.debug(f"{invoice_id = }")
    invoice = invoice_service.get_invoice_by_id(invoice_id)
    invoice_form = invoice_service.get_invoice_form()
    logger.debug(f"{invoice_form = }")
    if invoice_form.validate_on_submit():
        invoice_data = invoice_form.data
        logger.debug(f"{invoice_data = }")
        invoice = invoice_service.update_invoice_by_id(invoice_id, invoice_data)
        return render_template("invoices/invoice_detail.html", invoice=invoice)
    else:
        logger.error(f"{invoice_form.errors = }")
        return (
            render_template(
                "invoices/invoice_edit.html",
                invoice=invoice,
                invoice_form=invoice_form,
            ),
            422,
        )


@invoices_bp.route("/generate", methods=["POST"])
@login_required
@admin_user_required
def generate_invoice():
    # Add new invoice
    invoice_generate_form = invoice_service.get_invoice_generate_form()
    if invoice_generate_form.validate_on_submit():
        invoice_data = invoice_generate_form.data
        logger.debug(f"{invoice_data = }")
        invoice = invoice_service.generate_invoice(invoice_data=invoice_data)
        logger.debug(f"{invoice = }")
    else:
        logger.error(f"{invoice_generate_form.errors = }")
        return (
            render_template(
                "invoices/invoice_generate_form.html",
                invoice_generate_form=invoice_generate_form,
            ),
            422,
        )
    # Reset form
    invoice_generate_form = invoice_service.get_invoice_generate_form(
        ignore_request_data=True
    )
    return render_template(
        "invoices/invoice_generate_form.html",
        invoice_generate_form=invoice_generate_form,
    )


@invoices_bp.route("/<int:invoice_id>/download", methods=["GET"])
@login_required
@admin_user_required
def download_invoice_by_id(invoice_id: int):
    logger.debug(f"{invoice_id = }")
    result = invoice_service.download_invoice_by_id(invoice_id)
    logger.debug(f"{result = }")
    pdf_file, pdf_outpath = result
    return send_file(
        pdf_file,
        as_attachment=True,
        download_name=pdf_outpath,
        mimetype="application/pdf",
    )


@invoices_bp.route("/<int:invoice_id>", methods=["DELETE"])
@login_required
@admin_user_required
def delete_invoice_by_id(invoice_id: int):
    logger.debug(f"{invoice_id = }")
    invoice_service.delete_invoice_by_id(invoice_id)
    return ""
