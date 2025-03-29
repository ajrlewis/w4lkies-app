import datetime
from typing import Optional

from loguru import logger
from flask_login import current_user
from sqlalchemy import asc, desc, func

from app import db
from forms.vet_form import VetForm
from models.vet import Vet


def get_vet_form(
    vet: Optional[Vet] = None, ignore_request_data: bool = False
) -> VetForm:
    if ignore_request_data:
        logger.debug(f"{ignore_request_data = }")
        vet_form = VetForm(formdata=None)
    else:
        vet_form = VetForm()
    if vet:
        vet_form.name.data = vet.name
        vet_form.address.data = vet.address
        vet_form.phone.data = vet.phone
    return vet_form


def get_vets() -> list:
    # Generate query
    query = db.session.query(Vet).order_by(Vet.name.desc())
    vets = query.all()
    logger.debug(f"{vets = }")
    return vets


def get_vet_by_id(vet_id: int) -> Optional[Vet]:
    vet = db.session.get(Vet, vet_id)
    logger.debug(f"{vet = }")
    return vet


def update_vet_by_id(vet_id: int, vet_data: dict) -> Optional[Vet]:
    logger.debug(f"{vet_id = } {vet_data = }")
    vet = get_vet_by_id(vet_id)
    logger.debug(f"{vet = }")
    if not vet:
        logger.error(f"vet {vet_id} not found.")
        return

    if name := vet_data.get("name"):
        logger.debug(f"{name = }")
        vet.name = name

    if address := vet_data.get("address"):
        logger.debug(f"{address = }")
        vet.address = address

    if phone := vet_data.get("phone"):
        logger.debug(f"{phone = }")
        vet.phone = phone

    vet.updated_by = current_user.user_id
    vet.updated_at = datetime.datetime.now()

    try:
        db.session.commit()
        return vet
    except Exception as e:
        logger.error(f"Error updating vet: {e}")
        db.session.rollback()
        return


def add_vet(vet_data: dict) -> Optional[Vet]:
    new_vet = Vet(
        vet_id=vet_data.get("vet_id"),
        name=vet_data.get("name"),
        address=vet_data.get("address"),
        phone=vet_data.get("phone"),
    )
    try:
        db.session.add(new_vet)
        db.session.commit()
        logger.debug(f"{new_vet = }")
        return new_vet
    except Exception as e:
        logger.error(f"Error adding vet: {e}")
        db.session.rollback()
        return


def delete_vet_by_id(vet_id: int) -> None:
    vet = get_vet_by_id(vet_id)
    logger.debug(f"{vet = }")
    if vet is not None:
        try:
            db.session.delete(vet)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to delete vet: {e}")
    else:
        logger.error(f"Vet with ID {vet_id} does not exist")
