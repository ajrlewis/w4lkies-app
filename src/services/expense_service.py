import csv
import datetime
from typing import Optional

from loguru import logger
from sqlalchemy import asc, desc, func

from app import db
from forms.expense_form import ExpenseForm
from forms.expense_filter_form import ExpenseFilterForm
from models.expense import Expense


def get_expense_form(
    expense: Optional[Expense] = None, ignore_request_data: bool = False
) -> ExpenseForm:
    if ignore_request_data:
        expense_form = ExpenseForm(formdata=None)
    else:
        expense_form = ExpenseForm()
    if expense:
        expense_form.set_data_from_model(expense)
    return expense_form


def get_expense_filter_form() -> ExpenseFilterForm:
    expense_filter_form = ExpenseFilterForm()
    return expense_filter_form


def get_expense_categories() -> list:
    categories = [
        "Marketing",
        "Website",
        "Freelance",
        "Insurance",
        "Clothing",
        "Dog Treats / Games / Poo Bags",
        "Miscellaneous",
        "Entertainment",
        "Team Expenses",
        "Client Gifts",
        "Transportation",
    ]
    return sorted(categories)


def get_expenses(
    from_date: Optional[datetime.date] = None,
    to_date: Optional[datetime.date] = None,
    category: Optional[str] = None,
) -> list:
    # Generate query
    query = db.session.query(Expense).order_by(Expense.date.desc())

    # Filer expenses
    logger.debug(f"{from_date = } {to_date = } {category = }")
    if from_date:
        try:
            from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d").date()
            logger.debug(f"{from_date = }")
            query = query.filter(Expense.date >= from_date)
        except Exception as e:
            logger.error(f"{e = }")
    if to_date:
        try:
            to_date = datetime.datetime.strptime(to_date, "%Y-%m-%d").date()
            logger.debug(f"{to_date = }")
            query = query.filter(Expense.date <= to_date)
        except Exception as e:
            logger.error(f"{e = }")
    if category:
        try:
            query = query.filter(Expense.category == category)
        except Exception as e:
            logger.error(f"{e = }")

    expenses = query.all()
    logger.debug(f"{expenses = }")
    return expenses


def get_expense_by_id(expense_id: int) -> Optional[Expense]:
    expense = db.session.get(Expense, expense_id)
    logger.debug(f"{expense = }")
    return expense


def add_expense(expense_data: dict) -> Optional[Expense]:
    new_expense = Expense(
        date=expense_data.get("date"),
        category=expense_data.get("category"),
        price=expense_data.get("price"),
        description=expense_data.get("description"),
    )
    try:
        db.session.add(new_expense)
        db.session.commit()
        logger.debug(f"{new_expense = }")
        return new_expense
    except Exception as e:
        logger.error(f"Error adding expense: {e}")
        db.session.rollback()
        return


# def update_customer_by_id(customer_id: int, customer_data: dict) -> Optional[Customer]:
#     logger.debug(f"{customer_id = } {customer_data = }")

#     customer = get_customer_by_id(customer_id)
#     logger.debug(f"{customer = }")
#     if not customer:
#         logger.error(f"{customer_id} not found.")
#         return

#     if name := customer_data.get("name"):
#         logger.debug(f"{name = }")
#         customer.name = name

#     if phone := customer_data.get("phone"):
#         logger.debug(f"{phone = }")
#         customer.phone = phone

#     if email := customer_data.get("email"):
#         logger.debug(f"{email = }")
#         customer.email = email

#     if emergency_contact_name := customer_data.get("emergency_contact_name"):
#         logger.debug(f"{emergency_contact_name = }")
#         customer.emergency_contact_name = emergency_contact_name

#     if emergency_contact_phone := customer_data.get("emergency_contact_phone"):
#         logger.debug(f"{emergency_contact_phone = }")
#         customer.emergency_contact_phone = emergency_contact_phone

#     if signed_up_on := customer_data.get("signed_up_on"):
#         logger.debug(f"{signed_up_on = }")
#         customer.signed_up_on = signed_up_on

#     is_active = customer_data.get("is_active")
#     if is_active is not None:
#         logger.debug(f"{is_active = }")
#         customer.is_active = is_active

#     try:
#         db.session.commit()
#         return customer
#     except Exception as e:
#         logger.error(f"Error updating customer: {e}")
#         db.session.rollback()
#         return


def delete_expense_by_id(expense_id: int) -> None:
    expense = get_expense_by_id(expense_id)
    logger.debug(f"{expense = }")
    if expense is not None:
        try:
            db.session.delete(expense)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to delete expense: {e}")
    else:
        logger.error(f"Expense with ID {expense_id} does not exist")
