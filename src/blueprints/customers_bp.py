from flask import Blueprint, render_template, Response, request, send_from_directory
from flask_login import login_required
from loguru import logger

from services import customer_service


customers_bp = Blueprint("customers_bp", __name__)


@customers_bp.route("/base", methods=["GET"])
@login_required
def get_customers_base():
    return render_template("customers/customers_base.html")


@customers_bp.route("/info", methods=["GET"])
@login_required
def get_customers_info():
    customers = customer_service.get_customers()
    customer_filter_form = customer_service.get_customer_filter_form()
    logger.debug(f"{customers = } {customer_filter_form = }")
    return render_template(
        "customers/customers_info.html",
        customers=customers,
        customer_filter_form=customer_filter_form,
    )


@customers_bp.route("/", methods=["GET"])
@login_required
def get_customers():
    data = request.args.to_dict(flat=True)
    logger.debug(f"{data = }")
    customers = customer_service.get_customers(**data)
    logger.debug(f"{customers = }")
    return render_template("customers/customers.html", customers=customers)


@customers_bp.route("/<int:customer_id>", methods=["GET"])
@login_required
def get_customer_by_id(customer_id: int):
    customer = customer_service.get_customer_by_id(customer_id)
    logger.debug(f"{customer = }")
    if customer:
        return render_template("customers/customer_detail.html", customer=customer)
    return "", 404


@customers_bp.route("/add", methods=["GET"])
@login_required
def get_customer_form():
    customer_form = customer_service.get_customer_form()
    logger.debug(f"{customer_form = }")
    return render_template("customers/customer_form.html", customer_form=customer_form)


@customers_bp.route("/<int:customer_id>/edit", methods=["GET"])
@login_required
def edit_customer(customer_id: int):
    logger.debug(f"{customer_id = }")
    customer = customer_service.get_customer_by_id(customer_id)
    logger.debug(f"{customer = }")
    customer_form = customer_service.get_customer_form(customer)
    logger.debug(f"{customer_form = }")
    return render_template(
        "customers/customer_edit.html", customer=customer, customer_form=customer_form
    )


@customers_bp.route("/<int:customer_id>", methods=["PUT"])
@login_required
def update_customer(customer_id: int):
    logger.debug(f"{customer_id = }")
    customer = customer_service.get_customer_by_id(customer_id)
    customer_form = customer_service.get_customer_form()
    logger.debug(f"{customer_form = }")
    if customer_form.validate_on_submit():
        customer_data = customer_form.data
        logger.debug(f"{customer_data = }")
        customer = customer_service.update_customer_by_id(customer_id, customer_data)
        return render_template("customers/customer_detail.html", customer=customer)
    else:
        logger.error(f"{customer_form.errors = }")
        return (
            render_template(
                "customers/customer_edit.html",
                customer=customer,
                customer_form=customer_form,
            ),
            422,
        )


@customers_bp.route("/", methods=["POST"])
@login_required
def add_customer():
    # Add new customer
    customer_form = customer_service.get_customer_form()
    if customer_form.validate_on_submit():
        customer_data = customer_form.data
        # customer_data = customer_data | {"created_by": current_user.user_id}
        logger.debug(f"{customer_data = }")
        customer = customer_service.add_customer(customer_data=customer_data)
        logger.debug(f"{customer = }")
    else:
        logger.error(f"{customer_form.errors = }")
        return (
            render_template(
                "customers/customer_form.html", customer_form=customer_form
            ),
            422,
        )
    # Reset form
    customer_form = customer_service.get_customer_form(ignore_request_data=True)
    logger.debug(f"{customer_form = }")
    logger.debug(f"{customer_form.data = }")
    return render_template("customers/customer_form.html", customer_form=customer_form)


@customers_bp.route("/<int:customer_id>", methods=["DELETE"])
@login_required
def delete_customer_by_id(customer_id: int):
    logger.debug(f"{customer_id = }")
    customer_service.delete_customer_by_id(customer_id)
    return ""
