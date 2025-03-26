import datetime

from flask_wtf import FlaskForm
from wtforms.fields import BooleanField, DateField, StringField, SubmitField, TelField
from wtforms.validators import DataRequired, Optional, Regexp

from services import customer_service


class CustomerForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired()],
        render_kw={"placeholder": "Daphne Blake", "class": "u-full-width"},
    )

    phone = TelField(
        "Phone",
        validators=[
            DataRequired(),
            # Regexp(r"^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$"),
        ],
        render_kw={"placeholder": "(+44) 0123 456789", "class": "u-full-width"},
    )

    email = StringField(
        "Email",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "daphne@themysterymachine.com",
            "class": "u-full-width",
        },
    )

    emergency_contact_name = StringField(
        "Emergency Contact's Name",
        validators=[DataRequired()],
        render_kw={"placeholder": "Fred Jones", "class": "u-full-width"},
    )

    emergency_contact_phone = TelField(
        "Emergency Contact's Phone",
        validators=[
            DataRequired(),
            # Regexp(r"^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$"),
        ],
        render_kw={"placeholder": "(+44) 1234 567890", "class": "u-full-width"},
    )

    signed_up_on = DateField("Signed Up On", default=datetime.datetime.utcnow)

    is_active = BooleanField("Is active?", validators=[Optional()], default=True)
