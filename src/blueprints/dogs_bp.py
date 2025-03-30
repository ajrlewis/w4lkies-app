import datetime

from flask import Blueprint, render_template, Response, request, send_from_directory
from flask_login import current_user, login_required
from loguru import logger

from services import dog_service


dogs_bp = Blueprint("dogs_bp", __name__)


@dogs_bp.route("/base", methods=["GET"])
@login_required
def get_dogs_base():
    return render_template("dogs/dogs_base.html")


@dogs_bp.route("/info", methods=["GET"])
@login_required
def get_dogs_info():
    dogs = dog_service.get_dogs()
    logger.debug(f"{dogs = }")
    return render_template("dogs/dogs_info.html", dogs=dogs)


@dogs_bp.route("/", methods=["GET"])
@login_required
def get_dogs():
    data = request.args.to_dict(flat=True)
    logger.debug(f"{data = }")
    dogs = dog_service.get_dogs(**data)
    logger.debug(f"{dogs = }")
    return render_template("dogs/dogs.html", dogs=dogs)


@dogs_bp.route("/<int:dog_id>", methods=["GET"])
@login_required
def get_dog_by_id(dog_id: int):
    dog = dog_service.get_dog_by_id(dog_id)
    logger.debug(f"{dog = }")
    if dog:
        return render_template("dogs/dog_detail.html", dog=dog)
    return "", 404


@dogs_bp.route("/add", methods=["GET"])
@login_required
def get_dog_form():
    dog_form = dog_service.get_dog_form()
    logger.debug(f"{dog_form = }")
    return render_template("dogs/dog_form.html", dog_form=dog_form)


@dogs_bp.route("/<int:dog_id>/edit", methods=["GET"])
@login_required
def edit_dog(dog_id: int):
    logger.debug(f"{dog_id = }")
    dog = dog_service.get_dog_by_id(dog_id)
    logger.debug(f"{dog = }")
    dog_form = dog_service.get_dog_form(dog)
    logger.debug(f"{dog_form = }")
    return render_template("dogs/dog_edit.html", dog=dog, dog_form=dog_form)


@dogs_bp.route("/<int:dog_id>", methods=["PUT"])
@login_required
def update_dog(dog_id: int):
    logger.debug(f"{dog_id = }")
    dog = dog_service.get_dog_by_id(dog_id)
    dog_form = dog_service.get_dog_form()
    logger.debug(f"{dog_form = }")
    if dog_form.validate_on_submit():
        dog_data = dog_form.data
        dog_data = dog_data | {
            "updated_at": datetime.datetime.utcnow(),
            "updated_by": current_user.user_id,
        }
        logger.debug(f"{dog_data = }")
        dog = dog_service.update_dog_by_id(dog_id, dog_data)
        return render_template("dogs/dog_detail.html", dog=dog)
    else:
        logger.error(f"{dog_form.errors = }")
        return (
            render_template(
                "dogs/dog_edit.html",
                dog=dog,
                dog_form=dog_form,
            ),
            422,
        )


@dogs_bp.route("/", methods=["POST"])
@login_required
def add_dog():
    # Add new dog
    dog_form = dog_service.get_dog_form()
    if dog_form.validate_on_submit():
        dog_data = dog_form.data
        dog_data = dog_data | {"created_by": current_user.user_id}
        logger.debug(f"{dog_data = }")
        dog = dog_service.add_dog(dog_data=dog_data)
        logger.debug(f"{dog = }")
    else:
        logger.error(f"{dog_form.errors = }")
        return (
            render_template("dogs/dog_form.html", dog_form=dog_form),
            422,
        )
    # Reset form
    dog_form = dog_service.get_dog_form(ignore_request_data=True)
    logger.debug(f"{dog_form = }")
    logger.debug(f"{dog_form.data = }")
    return render_template("dogs/dog_form.html", dog_form=dog_form)


@dogs_bp.route("/<int:dog_id>", methods=["DELETE"])
@login_required
def delete_dog_by_id(dog_id: int):
    logger.debug(f"{dog_id = }")
    dog_service.delete_dog_by_id(dog_id)
    return ""
