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

from services import user_service


class BookingFilterForm(FlaskForm):
    user_id = SelectField("Filter by user", coerce=int, validators=[Optional()])
    date_min = DateField(
        "From this date",
        validators=[Optional()],
        format="%Y-%m-%d",
        render_kw={"placeholder": "yyyy-mm-dd"},
    )
    date_max = DateField(
        "Up to and including this date",
        validators=[Optional()],
        format="%Y-%m-%d",
        render_kw={"placeholder": "yyyy-mm-dd"},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_id_choices = [(-1, "All")] + [
            (user.user_id, user.name) for user in user_service.get_users()
        ]
        self.user_id.choices = user_id_choices
