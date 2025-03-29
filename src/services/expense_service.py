import csv
import datetime
from typing import Optional

from loguru import logger
from flask_login import current_user
from sqlalchemy import asc, desc, func

from app import db
from forms.expense_form import ExpenseForm
from forms.expense_filter_form import ExpenseFilterForm
from models.expense import Expense


def get_expense_form(
    expense: Optional[Expense] = None, ignore_request_data: bool = False
) -> ExpenseForm:
    if ignore_request_data:
        logger.debug(f"{ignore_request_data = }")
        expense_form = ExpenseForm(formdata=None)
    else:
        expense_form = ExpenseForm()
    if expense:
        expense_form.date.data = expense.date
        expense_form.price.data = expense.price
        expense_form.description.data = expense.description
        expense_form.category.data = expense.category
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
    if category and category != "All":
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


def update_expense_by_id(expense_id: int, expense_data: dict) -> Optional[Expense]:
    logger.debug(f"{expense_id = } {expense_data = }")
    expense = get_expense_by_id(expense_id)
    logger.debug(f"{expense = }")
    if not expense:
        logger.error(f"Expense {expense_id} not found.")
        return

    if date := expense_data.get("date"):
        logger.debug(f"{date = }")
        expense.date = date

    if category := expense_data.get("category"):
        logger.debug(f"{category = }")
        expense.category = category

    if price := expense_data.get("price"):
        logger.debug(f"{price = }")
        expense.price = price

    if description := expense_data.get("description"):
        logger.debug(f"{description = }")
        expense.description = description

    expense.updated_by = current_user.user_id
    expense.updated_at = datetime.datetime.now()

    try:
        db.session.commit()
        return expense
    except Exception as e:
        logger.error(f"Error updating expense: {e}")
        db.session.rollback()
        return


def add_expense(expense_data: dict) -> Optional[Expense]:
    new_expense = Expense(
        expense_id=expense_data.get("expense_id"),
        date=expense_data.get("date"),
        category=expense_data.get("category"),
        price=expense_data.get("price"),
        description=expense_data.get("description"),
        created_at=expense_data.get("created_at"),
        created_by=expense_data.get("created_by"),
        updated_at=expense_data.get("updated_at"),
        updated_by=expense_data.get("updated_by"),
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
