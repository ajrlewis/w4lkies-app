from datetime import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    BooleanField,
    DateField,
    DecimalField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Optional

from services import service_service


class ServiceForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter the name of the service"},
    )

    description = TextAreaField(
        "Description",
        validators=[Optional()],
        render_kw={"placeholder": "A description of the service"},
    )

    price = DecimalField(
        "Price / £",
        validators=[DataRequired()],
        render_kw={"placeholder": "The price of the service"},
    )

    duration = DecimalField(
        "Duration / minutes",
        validators=[Optional()],
        render_kw={"placeholder": "The duration of the service"},
    )

    is_publicly_offered = BooleanField(
        "Is offered to the public?",
        validators=[Optional()],
        default=False,
    )

    is_active = BooleanField(
        "Is active?",
        validators=[Optional()],
        default=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
