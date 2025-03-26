import datetime

from flask_wtf import FlaskForm
from wtforms.fields import BooleanField, DateField, StringField, SubmitField, TelField
from wtforms.validators import DataRequired, Optional, Regexp

from services import vet_service


class VetForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter the vet name"},
    )

    address = StringField(
        "Address",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter the vet address"},
    )

    phone = TelField(
        "Phone",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter the vet phone number"},
    )
