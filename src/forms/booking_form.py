from datetime import date, datetime, timedelta, time

from flask_wtf import FlaskForm
from loguru import logger
from wtforms import (
    BooleanField,
    DateField,
    IntegerField,
    SelectField,
    SubmitField,
)
from wtforms.validators import DataRequired, Optional

from services import (
    booking_service,
    customer_service,
    service_service,
    user_service,
    vet_service,
)


def get_time_choices(start_hour: int, end_hour: int, interval_minutes: int):
    working_hours_start = time(start_hour, 0)
    working_hours_end = time(end_hour, 0)
    time_interval = timedelta(minutes=interval_minutes)
    time_choices = []
    current_time = datetime.combine(datetime.today(), working_hours_start)
    end_time = datetime.combine(datetime.today(), working_hours_end)
    while current_time <= end_time:
        time_choice = (
            current_time.strftime("%H:%M:%S"),
            current_time.strftime("%I:%M %p"),
        )
        time_choices.append(time_choice)
        current_time += time_interval
    logger.debug(f"{time_choices = }")
    return time_choices


class BookingForm(FlaskForm):
    date = DateField(
        "On this date",
        validators=[DataRequired()],
        format="%Y-%m-%d",
        render_kw={"placeholder": "yyyy-mm-dd"},
    )
    time = SelectField("At this time", validators=[DataRequired()])
    user_id = SelectField("Assign", coerce=int, validators=[DataRequired()])
    service_id = SelectField("The following", coerce=int, validators=[DataRequired()])
    customer_id = SelectField("For owner", coerce=int, validators=[DataRequired()])
    repeating_weeks = IntegerField(
        "Repeat for number of weeks", default=0, validators=[Optional()]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.time.choices = get_time_choices(
            start_hour=8, end_hour=18, interval_minutes=15
        )

        self.user_id.choices = [
            (user.user_id, user.name) for user in user_service.get_users()
        ]

        self.customer_id.choices = [
            (customer.customer_id, customer.name)
            for customer in customer_service.get_customers(is_active=True)
        ]

        self.service_id.choices = [
            (service.service_id, service.name)
            for service in service_service.get_services(is_active=True)
        ]
