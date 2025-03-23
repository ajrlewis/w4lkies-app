from flask import Blueprint, render_template, Response, request, send_from_directory
from flask_login import login_required
from loguru import logger

from services import expense_service


expenses_bp = Blueprint("expenses_bp", __name__)


@expenses_bp.route("/base", methods=["GET"])
@login_required
def get_expenses_base():
    return render_template("expenses/expenses_base.html")


@expenses_bp.route("/info", methods=["GET"])
@login_required
def get_expenses_info():
    expenses = expense_service.get_expenses()
    expense_filter_form = expense_service.get_expense_filter_form()
    logger.debug(f"{expenses = } {expense_filter_form = }")
    return render_template(
        "expenses/expenses_info.html",
        expenses=expenses,
        expense_filter_form=expense_filter_form,
    )


@expenses_bp.route("/", methods=["GET"])
@login_required
def get_expenses():
    data = request.args.to_dict(flat=True)
    logger.debug(f"{data = }")
    expenses = expense_service.get_expenses(**data)
    logger.debug(f"{expenses = }")
    return render_template("expenses/expenses.html", expenses=expenses)


@expenses_bp.route("/<int:expense_id>", methods=["GET"])
@login_required
def get_expense_by_id(expense_id: int):
    expense = expense_service.get_expense_by_id(expense_id)
    logger.debug(f"{expense = }")
    if expense:
        return render_template("expenses/expense_detail.html", expense=expense)
    return "", 404


@expenses_bp.route("/add", methods=["GET"])
@login_required
def get_expense_form():
    expense_form = expense_service.get_expense_form()
    logger.debug(f"{expense_form = }")
    return render_template("expenses/expense_form.html", expense_form=expense_form)


@expenses_bp.route("/<int:expense_id>/edit", methods=["GET"])
@login_required
def edit_expense(expense_id: int):
    logger.debug(f"{expense_id = }")
    expense = expense_service.get_expense_by_id(expense_id)
    logger.debug(f"{expense = }")
    expense_form = expense_service.get_expense_form(expense)
    logger.debug(f"{expense_form = }")
    return render_template(
        "expenses/expense_edit.html", expense=expense, expense_form=expense_form
    )


@expenses_bp.route("/<int:expense_id>", methods=["PUT"])
@login_required
def update_expense(expense_id: int):
    logger.debug(f"{expense_id = }")
    expense = expense_service.get_expense_by_id(expense_id)
    expense_form = expense_service.get_expense_form()
    logger.debug(f"{expense_form = }")
    if expense_form.validate_on_submit():
        expense_data = expense_form.data
        logger.debug(f"{expense_data = }")
        expense = expense_service.update_expense_by_id(expense_id, expense_data)
        return render_template("expense_detail.html", expense=expense)
    else:
        logger.error(f"{expense_form.errors = }")
        return (
            render_template(
                "expenses/expense_edit.html", expense=expense, expense_form=expense_form
            ),
            422,
        )


@expenses_bp.route("/", methods=["POST"])
@login_required
def add_expense():
    # Add new expense
    expense_form = expense_service.get_expense_form()
    if expense_form.validate_on_submit():
        expense_data = expense_form.data
        # expense_data = expense_data | {"created_by": current_user.user_id}
        logger.debug(f"{expense_data = }")
        expense = expense_service.add_expense(expense_data=expense_data)
        logger.debug(f"{expense = }")
    else:
        logger.error(f"{expense_form.errors = }")
        return (
            render_template("expenses/expense_form.html", expense_form=expense_form),
            422,
        )
    # Reset form
    expense_form = expense_service.get_expense_form(ignore_request_data=True)
    logger.debug(f"{expense_form = }")
    logger.debug(f"{expense_form.data = }")
    return render_template("expenses/expense_form.html", expense_form=expense_form)


@expenses_bp.route("/<int:expense_id>", methods=["DELETE"])
@login_required
def delete_expense_by_id(expense_id: int):
    logger.debug(f"{expense_id = }")
    expense_service.delete_expense_by_id(expense_id)
    return ""
