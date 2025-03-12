from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TelField
from wtforms.validators import DataRequired, Optional
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp


class UserForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired(message="Enter a valid name.")],
        render_kw={
            "placeholder": "Foo Bar",
            "class": "u-full-width",
        },
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(message="Invalid email address"),
            Length(max=254, message="Email address is too long"),
        ],
        render_kw={
            "placeholder": "Enter your email address",
            "autocomplete": "email",
            "type": "email",
        },
    )

    is_admin = BooleanField("Admin", validators=[Optional()])

    # password = PasswordField(
    #     "Password",
    #     validators=[DataRequired()],
    #     render_kw={"placeholder": "*****", "class": "u-full-width"},
    # )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters long"),
            # Regexp(
            #     r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$",
            #     message="Password must contain at least one lowercase letter, one uppercase letter, one digit and one special character",
            # ),
        ],
        render_kw={"placeholder": "Enter your password", "autocomplete": "off"},
    )
