import datetime

from flask_wtf import FlaskForm
from wtforms.fields import DateField, DecimalField, SelectField, StringField
from wtforms.validators import DataRequired, Optional

from services import expense_service


class ExpenseForm(FlaskForm):
    date = DateField(
        "Date",
        validators=[DataRequired()],
        format="%Y-%m-%d",
        default=datetime.date.today(),
    )
    category = SelectField("Category", validators=[Optional()])
    price = DecimalField("Price", validators=[DataRequired()])
    description = StringField("Description", validators=[Optional()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        category_choices = expense_service.get_expense_categories()
        self.category.choices = category_choices
