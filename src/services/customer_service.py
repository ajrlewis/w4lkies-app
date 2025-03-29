import datetime
from typing import Optional

from loguru import logger
from flask_login import current_user
from sqlalchemy import asc, desc, func

from app import db
from forms.customer_form import CustomerForm
from forms.customer_filter_form import CustomerFilterForm
from models.customer import Customer


def get_customer_form(
    customer: Optional[Customer] = None, ignore_request_data: bool = False
) -> CustomerForm:
    if ignore_request_data:
        logger.debug(f"{ignore_request_data = }")
        customer_form = CustomerForm(formdata=None)
    else:
        customer_form = CustomerForm()
    if customer:
        customer_form.name.data = customer.name
        customer_form.phone.data = customer.phone
        customer_form.email.data = customer.email
        customer_form.emergency_contact_name.data = customer.emergency_contact_name
        customer_form.emergency_contact_phone.data = customer.emergency_contact_phone
        customer_form.signed_up_on.data = customer.signed_up_on
        customer_form.is_active.data = customer.is_active
    return customer_form


def get_customer_filter_form() -> CustomerFilterForm:
    customer_filter_form = CustomerFilterForm()
    return customer_filter_form


def get_customers(is_active: Optional[bool] = None) -> list:
    # Generate query
    query = db.session.query(Customer).order_by(Customer.name.desc())

    # Filer customers
    if is_active and is_active != "All":
        try:
            is_active = f"{is_active}".lower() == "true"
            logger.debug(f"{is_active = }")
            query = query.filter(Customer.is_active == is_active)
        except Exception as e:
            logger.error(f"{e = }")

    customers = query.all()
    logger.debug(f"{customers = }")
    return customers


def get_customer_by_id(customer_id: int) -> Optional[Customer]:
    customer = db.session.get(Customer, customer_id)
    logger.debug(f"{customer = }")
    return customer


def update_customer_by_id(customer_id: int, customer_data: dict) -> Optional[Customer]:
    logger.debug(f"{customer_id = } {customer_data = }")
    customer = get_customer_by_id(customer_id)
    logger.debug(f"{customer = }")
    if not customer:
        logger.error(f"Customer {customer_id} not found.")
        return

    if name := customer_data.get("name"):
        logger.debug(f"{name = }")
        customer.name = name

    if phone := customer_data.get("phone"):
        logger.debug(f"{phone = }")
        customer.phone = phone

    if email := customer_data.get("email"):
        logger.debug(f"{email = }")
        customer.email = email

    if emergency_contact_name := customer_data.get("emergency_contact_name"):
        logger.debug(f"{emergency_contact_name = }")
        customer.emergency_contact_name = emergency_contact_name

    if emergency_contact_phone := customer_data.get("emergency_contact_phone"):
        logger.debug(f"{emergency_contact_phone = }")
        customer.emergency_contact_phone = emergency_contact_phone

    if signed_up_on := customer_data.get("signed_up_on"):
        logger.debug(f"{signed_up_on = }")
        customer.signed_up_on = signed_up_on

    is_active = customer_data.get("is_active")
    if is_active is not None:
        logger.debug(f"{is_active = }")
        customer.is_active = is_active

    customer.updated_by = current_user.user_id
    customer.updated_at = datetime.datetime.now()

    try:
        db.session.commit()
        return customer
    except Exception as e:
        logger.error(f"Error updating customer: {e}")
        db.session.rollback()
        return


def add_customer(customer_data: dict) -> Optional[Customer]:
    new_customer = Customer(
        customer_id=customer_data.get("customer_id"),
        name=customer_data.get("name"),
        phone=customer_data.get("phone"),
        email=customer_data.get("email"),
        emergency_contact_name=customer_data.get("emergency_contact_name"),
        emergency_contact_phone=customer_data.get("emergency_contact_phone"),
        signed_up_on=customer_data.get("signed_up_on"),
        is_active=customer_data.get("is_active"),
        created_at=customer_data.get("created_at"),
        created_by=customer_data.get("created_by"),
        updated_at=customer_data.get("updated_at"),
        updated_by=customer_data.get("updated_by"),
    )
    try:
        db.session.add(new_customer)
        db.session.commit()
        logger.debug(f"{new_customer = }")
        return new_customer
    except Exception as e:
        logger.error(f"Error adding customer: {e}")
        db.session.rollback()
        return


def delete_customer_by_id(customer_id: int) -> None:
    customer = get_customer_by_id(customer_id)
    logger.debug(f"{customer = }")
    if customer is not None:
        try:
            db.session.delete(customer)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to delete customer: {e}")
    else:
        logger.error(f"Customer with ID {customer_id} does not exist")
