from datetime import date

from flask_wtf import FlaskForm
from wtforms.fields import DateField, SelectField, StringField
from wtforms.validators import DataRequired, Optional

from services import customer_service


class CustomerFilterForm(FlaskForm):
    class Meta:
        csrf = False

    is_active = SelectField("Active", validators=[Optional()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        is_active_choices = ["All", True, False]
        self.is_active.choices = is_active_choices
