import datetime
from typing import Optional

from loguru import logger
from flask_login import current_user
from sqlalchemy import asc, desc, func

from app import db
from forms.service_form import ServiceForm
from models.service import Service


def get_service_form(
    service: Optional[Service] = None, ignore_request_data: bool = False
) -> ServiceForm:
    if ignore_request_data:
        logger.debug(f"{ignore_request_data = }")
        service_form = ServiceForm(formdata=None)
    else:
        service_form = ServiceForm()
    if service:
        service_form.name.data = service.name
        service_form.description.data = service.description
        service_form.price.data = service.price
        service_form.duration.data = service.duration
        service_form.is_active.data = service.is_active
    return service_form


def get_services(is_active: Optional[bool] = None) -> list:
    # Generate query
    query = db.session.query(Service).order_by(Service.name.desc())
    if is_active and is_active != "All":
        try:
            is_active = f"{is_active}".lower() == "true"
            logger.debug(f"{is_active = }")
            query = query.filter(Service.is_active == is_active)
        except Exception as e:
            logger.error(f"{e = }")
    services = query.all()
    logger.debug(f"{services = }")
    return services


def get_service_by_id(service_id: int) -> Optional[Service]:
    service = db.session.get(Service, service_id)
    logger.debug(f"{service = }")
    return service


def update_service_by_id(service_id: int, service_data: dict) -> Optional[Service]:
    logger.debug(f"{service_id = } {service_data = }")
    service = get_service_by_id(service_id)
    logger.debug(f"{service = }")
    if not service:
        logger.error(f"service {service_id} not found.")
        return

    if name := service_data.get("name"):
        logger.debug(f"{name = }")
        service.name = name

    if price := service_data.get("price"):
        logger.debug(f"{price = }")
        service.price = price

    if description := service_data.get("description"):
        logger.debug(f"{description = }")
        service.description = description

    if duration := service_data.get("duration"):
        logger.debug(f"{duration = }")
        service.duration = duration

    is_publicly_offered = service_data.get("is_publicly_offered")
    if is_publicly_offered is not None:
        service.is_publicly_offered = is_publicly_offered

    is_active = service_data.get("is_active")
    if is_active is not None:
        service.is_active = is_active

    service.updated_by = current_user.user_id
    service.updated_at = datetime.datetime.now()

    try:
        db.session.commit()
        return service
    except Exception as e:
        logger.error(f"Error updating service: {e}")
        db.session.rollback()
        return


def add_service(service_data: dict) -> Optional[Service]:
    new_service = Service(
        name=service_data.get("name"),
        price=service_data.get("price"),
        description=service_data.get("description"),
        duration=service_data.get("duration"),
        is_publicly_offered=service_data.get("is_publicly_offered"),
        is_active=service_data.get("is_active"),
        created_by=current_user.user_id,
    )
    try:
        db.session.add(new_service)
        db.session.commit()
        logger.debug(f"{new_service = }")
        return new_service
    except Exception as e:
        logger.error(f"Error adding service: {e}")
        db.session.rollback()
        return


def delete_service_by_id(service_id: int) -> None:
    service = get_service_by_id(service_id)
    logger.debug(f"{service = }")
    if service is not None:
        try:
            db.session.delete(service)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to delete service: {e}")
    else:
        logger.error(f"Service with ID {service_id} does not exist")
