from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TelField
from wtforms.validators import DataRequired, Optional

# from utils.form_mixin import FormMixin


class UserForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "Foo Bar",
            "class": "u-full-width",
        },
    )

    email = StringField(
        "Email",
        validators=[DataRequired()],
        render_kw={"placeholder": "foo@bar.com", "class": "u-full-width"},
    )

    is_admin = BooleanField("Admin", validators=[Optional()])

    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "*****", "class": "u-full-width"},
    )
