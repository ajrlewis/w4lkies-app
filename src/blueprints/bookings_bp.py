import datetime

from flask import Blueprint, render_template, Response, request, send_from_directory
from flask_login import current_user, login_required
from loguru import logger

from services import booking_service


bookings_bp = Blueprint("bookings_bp", __name__)


@bookings_bp.route("/base", methods=["GET"])
@login_required
def get_bookings_base():
    return render_template("bookings/bookings_base.html")


@bookings_bp.route("/info", methods=["GET"])
@login_required
def get_bookings_info():
    bookings = booking_service.get_bookings()
    bookings = bookings[:50]
    booking_filter_form = booking_service.get_booking_filter_form()
    logger.debug(f"{bookings = }")
    return render_template(
        "bookings/bookings_info.html",
        bookings=bookings,
        booking_filter_form=booking_filter_form,
    )


@bookings_bp.route("/", methods=["GET"])
@login_required
def get_bookings():
    data = request.args.to_dict(flat=True)
    logger.debug(f"{data = }")
    bookings = booking_service.get_bookings(**data)
    bookings = bookings[:50]
    logger.debug(f"{bookings = }")
    return render_template("bookings/bookings.html", bookings=bookings)


@bookings_bp.route("/<int:booking_id>", methods=["GET"])
@login_required
def get_booking_by_id(booking_id: int):
    booking = booking_service.get_booking_by_id(booking_id)
    logger.debug(f"{booking = }")
    if booking:
        return render_template("bookings/booking_detail.html", booking=booking)
    return "", 404


@bookings_bp.route("/add", methods=["GET"])
@login_required
def get_booking_form():
    booking_form = booking_service.get_booking_form()
    logger.debug(f"{booking_form = }")
    return render_template("bookings/booking_form.html", booking_form=booking_form)


@bookings_bp.route("/<int:booking_id>/edit", methods=["GET"])
@login_required
def edit_booking(booking_id: int):
    logger.debug(f"{booking_id = }")
    booking = booking_service.get_booking_by_id(booking_id)
    logger.debug(f"{booking = }")
    booking_form = booking_service.get_booking_form(booking)
    logger.debug(f"{booking_form = }")
    return render_template(
        "bookings/booking_edit.html", booking=booking, booking_form=booking_form
    )


@bookings_bp.route("/<int:booking_id>", methods=["PUT"])
@login_required
def update_booking(booking_id: int):
    logger.debug(f"{booking_id = }")
    booking = booking_service.get_booking_by_id(booking_id)
    booking_form = booking_service.get_booking_form()
    logger.debug(f"{booking_form = }")
    if booking_form.validate_on_submit():
        booking_data = booking_form.data
        booking_data = booking_data | {
            "updated_at": current_user.user_id,
            "updated_by": datetime.datetime.utcnow(),
        }
        logger.debug(f"{booking_data = }")
        booking = booking_service.update_booking_by_id(booking_id, booking_data)
        return render_template("bookings/booking_detail.html", booking=booking)
    else:
        logger.error(f"{booking_form.errors = }")
        return (
            render_template(
                "bookings/booking_edit.html",
                booking=booking,
                booking_form=booking_form,
            ),
            422,
        )


@bookings_bp.route("/", methods=["POST"])
@login_required
def add_booking():
    # Add new booking
    booking_form = booking_service.get_booking_form()
    if booking_form.validate_on_submit():
        booking_data = booking_form.data
        booking_data = booking_data | {"created_by": current_user.user_id}
        logger.debug(f"{booking_data = }")
        bookings = booking_service.add_booking(booking_data=booking_data)
        logger.debug(f"{bookings = }")
    else:
        logger.error(f"{booking_form.errors = }")
        return (
            render_template("bookings/booking_form.html", booking_form=booking_form),
            422,
        )
    # Reset form to last booking
    booking_form = booking_service.get_booking_form(
        booking=bookings[0], ignore_request_data=True
    )
    logger.debug(f"{booking_form = }")
    logger.debug(f"{booking_form.data = }")
    return render_template("bookings/booking_form.html", booking_form=booking_form)


@bookings_bp.route("/<int:booking_id>", methods=["DELETE"])
@login_required
def delete_booking_by_id(booking_id: int):
    logger.debug(f"{booking_id = }")
    booking_service.delete_booking_by_id(booking_id)
    return ""
