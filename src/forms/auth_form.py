from datetime import date

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

from forms.user_form import UserForm


class AuthForm(FlaskForm):
    email = UserForm.email

    password = UserForm.password
