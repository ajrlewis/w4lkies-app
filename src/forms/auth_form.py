from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class AuthForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired()],
        render_kw={"placeholder": "daphne@themysterymachine.com"},
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Creeps and Crawls!"},
    )
