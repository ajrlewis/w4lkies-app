import datetime
from typing import Optional

from loguru import logger
from flask_login import current_user
from sqlalchemy import desc

from app import db
from forms.booking_form import BookingForm
from forms.booking_filter_form import BookingFilterForm
from models.booking import Booking

booking_date_format = "%Y-%m-%d"
booking_time_format = "%H:%M:%S"
booking_datetime_format = f"{booking_date_format} {booking_time_format}"


def get_booking_form(
    booking: Optional[Booking] = None, ignore_request_data: bool = False
) -> BookingForm:
    if ignore_request_data:
        logger.debug(f"{ignore_request_data = }")
        booking_form = BookingForm(formdata=None)
    else:
        booking_form = BookingForm()
    if booking:
        # booking_form.date.data = booking.date.strftime(booking_date_format)
        # booking_form.time.data = booking.time.strftime(booking_time_format)
        booking_form.date.data = booking.date
        booking_form.time.data = booking.time.strftime("%H:%M:%S")
        logger.debug(f"{booking_form.time.data = } {booking.time = }")
        booking_form.customer_id.data = booking.customer_id
        booking_form.service_id.data = booking.service_id
        # booking_form.invoice_id.data = booking.invoice_id
        booking_form.user_id.data = booking.user_id
    return booking_form


def get_booking_filter_form() -> BookingFilterForm:
    booking_filter_form = BookingFilterForm()
    return booking_filter_form


def get_booking_by_id(booking_id: int) -> Booking:
    booking = db.session.get(Booking, booking_id)
    return booking


def get_bookings(
    user_id: Optional[int] = None,
    customer_id: Optional[int] = None,
    date_min: Optional[str] = None,
    date_max: Optional[str] = None,
    order_by: Optional[tuple] = (Booking.date.desc(), Booking.time.asc()),
) -> list[Booking]:
    query = db.session.query(Booking)
    if user_id and int(user_id) > -1:
        query = query.filter(Booking.user_id == user_id)
    if customer_id and int(customer_id) > -1:
        query = query.filter(Booking.customer_id == customer_id)
    if date_min:
        query = query.filter(Booking.date >= date_min)
    if date_max:
        query = query.filter(Booking.date <= date_max)
    if order_by:
        query = query.order_by(*order_by)
    bookings = query.all()
    return bookings


def get_booking_datetime(booking: Booking):
    datetime_string = " ".join(
        [
            booking.date.strftime(booking_date_format),
            booking.time.strftime(booking_time_format),
        ]
    )
    booking_datetime = datetime.datetime.strptime(
        datetime_string, booking_datetime_format
    )
    return booking_datetime


def get_repeating_booking_datetimes(booking: Booking, repeating_weeks: int) -> list:
    booking_datetime = get_booking_datetime(booking)
    next_booking_datetimes = []
    for i in range(repeating_weeks):
        delta_datetime = datetime.timedelta(days=(i + 1) * 7)
        next_booking_datetime = booking_datetime + delta_datetime
        next_booking_datetimes.append(next_booking_datetime)
    logger.debug(f"{next_booking_datetimes = }")
    return next_booking_datetimes


def add_booking(booking_data: dict) -> list[Booking]:
    if booking_data.get("repeating_weeks", 0) > 0:
        bookings = add_repeat_bookings(booking_data=booking_data)
    else:
        booking = add_single_booking(booking_data=booking_data)
        bookings = [booking]
    logger.debug(f"{bookings = }")
    return bookings


def add_single_booking(booking_data: dict) -> Optional[Booking]:
    time = datetime.datetime.strptime(booking_data.get("time"), booking_time_format)
    new_booking = Booking(
        booking_id=booking_data.get("booking_id"),
        date=booking_data.get("date"),
        time=time,
        customer_id=booking_data.get("customer_id"),
        service_id=booking_data.get("service_id"),
        invoice_id=booking_data.get("invoice_id"),
        user_id=booking_data.get("user_id"),
        created_at=booking_data.get("created_at"),
        created_by=booking_data.get("created_by"),
    )
    try:
        db.session.add(new_booking)
        db.session.commit()
        logger.debug(f"{new_booking = }")
        return new_booking
    except Exception as e:
        logger.error(f"Error adding booking: {e}")
        db.session.rollback()
        return


def add_repeat_bookings(booking_data: dict) -> list[Booking]:
    booking = add_single_booking(booking_data=booking_data)
    if not booking:
        return []
    bookings = [booking]
    logger.debug(f"{bookings = }")
    repeating_weeks = booking_data.get("repeating_weeks")
    logger.debug(f"{repeating_weeks = }")
    if repeating_weeks > 0:
        datetimes = get_repeating_booking_datetimes(booking, repeating_weeks)
        logger.debug(f"{datetimes = }")
        for datetime in datetimes:
            logger.debug(f"{datetime = }")
            repeat_booking_data = booking_data.copy()
            repeat_booking_data["date"] = f"{datetime.date()}"
            repeat_booking_data["time"] = f"{datetime.time()}"
            repeat_booking = add_single_booking(repeat_booking_data)
            if repeat_booking:
                bookings.append(repeat_booking)
    logger.debug(f"{bookings = }")
    return bookings


def update_booking_by_id(booking_id: int, booking_data: dict) -> Optional[Booking]:
    logger.debug(f"{booking_id = } {booking_data = }")
    booking = get_booking_by_id(booking_id)
    logger.debug(f"{booking = }")
    if not booking:
        logger.error(f"booking {booking_id} not found.")
        return

    if date := booking_data.get("date"):
        logger.debug(f"{date = }")
        booking.date = date

    if time := booking_data.get("time"):
        booking.time = time

    if customer_id := booking_data.get("customer_id"):
        logger.debug(f"{customer_id = }")
        booking.customer_id = customer_id

    if service_id := booking_data.get("service_id"):
        logger.debug(f"{service_id = }")
        booking.service_id = service_id

    if invoice_id := booking_data.get("invoice_id"):
        logger.debug(f"{invoice_id = }")
        booking.invoice_id = invoice_id

    if user_id := booking_data.get("user_id"):
        logger.debug(f"{user_id = }")
        booking.user_id = user_id

    booking.updated_by = current_user.user_id
    booking.updated_at = datetime.datetime.now()

    try:
        db.session.commit()
        return booking
    except Exception as e:
        logger.error(f"Error updating booking: {e}")
        db.session.rollback()
        return


def delete_booking_by_id(booking_id: int) -> None:
    booking = get_booking_by_id(booking_id)
    logger.debug(f"{booking = }")
    if booking is not None:
        try:
            db.session.delete(booking)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to delete booking: {e}")
    else:
        logger.error(f"Booking with ID {booking_id} does not exist")
