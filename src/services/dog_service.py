import datetime
from typing import Optional

from loguru import logger
from sqlalchemy import asc, desc, func

from app import db
from forms.dog_form import DogForm
from models.dog import Dog


def get_dog_form(
    dog: Optional[Dog] = None, ignore_request_data: bool = False
) -> DogForm:
    if ignore_request_data:
        logger.debug(f"{ignore_request_data = }")
        dog_form = DogForm(formdata=None)
    else:
        dog_form = DogForm()
    if dog:
        dog_form.name.data = dog.name
        dog_form.date_of_birth.data = dog.date_of_birth
        dog_form.is_allowed_treats.data = dog.is_allowed_treats
        dog_form.is_allowed_off_the_lead.data = dog.is_allowed_off_the_lead
        dog_form.is_allowed_on_social_media.data = dog.is_allowed_on_social_media
        dog_form.is_neutered_or_spayed.data = dog.is_neutered_or_spayed
        dog_form.behavioral_issues.data = dog.behavioral_issues
        dog_form.medical_needs.data = dog.medical_needs
        dog_form.breed.data = dog.breed
        dog_form.customer_id.data = dog.customer_id
        dog_form.vet_id.data = dog.vet_id
    return dog_form


def get_dogs() -> list:
    # Generate query
    query = db.session.query(Dog).order_by(Dog.name.desc())
    dogs = query.all()
    logger.debug(f"{dogs = }")
    return dogs


def get_dog_by_id(dog_id: int) -> Optional[Dog]:
    dog = db.session.get(Dog, dog_id)
    logger.debug(f"{dog = }")
    return dog


def update_dog_by_id(dog_id: int, dog_data: dict) -> Optional[Dog]:
    logger.debug(f"{dog_id = } {dog_data = }")
    dog = get_dog_by_id(dog_id)
    logger.debug(f"{dog = }")
    if not dog:
        logger.error(f"Dog {dog_id} not found.")
        return

    if name := dog_data.get("name"):
        logger.debug(f"{name = }")
        dog.name = name

    if date_of_birth := dog_data.get("date_of_birth"):
        logger.debug(f"{date_of_birth = }")
        dog.date_of_birth = date_of_birth

    is_allowed_treats = dog_data.get("is_allowed_treats")
    if is_allowed_treats is not None:
        dog.is_allowed_treats = is_allowed_treats

    is_allowed_off_the_lead = dog_data.get("is_allowed_off_the_lead")
    if is_allowed_off_the_lead is not None:
        dog.is_allowed_off_the_lead = is_allowed_off_the_lead

    is_allowed_on_social_media = dog_data.get("is_allowed_on_social_media")
    if is_allowed_on_social_media is not None:
        dog.is_allowed_on_social_media = is_allowed_on_social_media

    is_neutered_or_spayed = dog_data.get("is_neutered_or_spayed")
    if is_neutered_or_spayed is not None:
        dog.is_neutered_or_spayed = is_allowed_treats

    if behavioral_issues := dog_data.get("behavioral_issues"):
        logger.debug(f"{behavioral_issues = }")
        dog.behavioral_issues = behavioral_issues

    if medical_needs := dog_data.get("medical_needs"):
        logger.debug(f"{medical_needs = }")
        dog.medical_needs = medical_needs

    if breed := dog_data.get("breed"):
        logger.debug(f"{breed = }")
        dog.breed = breed

    if customer_id := dog_data.get("customer_id"):
        logger.debug(f"{customer_id = }")
        dog.customer_id = customer_id

    if vet_id := dog_data.get("vet_id"):
        logger.debug(f"{vet_id = }")
        dog.vet_id = vet_id

    # dog.updated_by = current_user.user_id
    # dog.updated_at = datetime.datetime.now()

    try:
        db.session.commit()
        return dog
    except Exception as e:
        logger.error(f"Error updating dog: {e}")
        db.session.rollback()
        return


def add_dog(dog_data: dict) -> Optional[Dog]:
    new_dog = Dog(
        dog_id=dog_data.get("dog_id"),
        name=dog_data.get("name"),
        date_of_birth=dog_data.get("date_of_birth"),
        is_allowed_treats=dog_data.get("is_allowed_treats"),
        is_allowed_off_the_lead=dog_data.get("is_allowed_off_the_lead"),
        is_allowed_on_social_media=dog_data.get("is_allowed_on_social_media"),
        is_neutered_or_spayed=dog_data.get("is_neutered_or_spayed"),
        behavioral_issues=dog_data.get("behavioral_issues"),
        medical_needs=dog_data.get("medical_needs"),
        breed=dog_data.get("breed"),
        customer_id=dog_data.get("customer_id"),
        vet_id=dog_data.get("vet_id"),
        created_at=dog_data.get("created_at"),
        created_by=dog_data.get("created_by"),
        updated_at=dog_data.get("updated_at"),
        updated_by=dog_data.get("updated_by"),
    )
    try:
        db.session.add(new_dog)
        db.session.commit()
        logger.debug(f"{new_dog = }")
        return new_dog
    except Exception as e:
        logger.error(f"Error adding dog: {e}")
        db.session.rollback()
        return


def delete_dog_by_id(dog_id: int) -> None:
    dog = get_dog_by_id(dog_id)
    logger.debug(f"{dog = }")
    if dog is not None:
        try:
            db.session.delete(dog)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to delete dog: {e}")
    else:
        logger.error(f"dog with ID {dog_id} does not exist")
