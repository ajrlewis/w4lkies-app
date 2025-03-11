from datetime import date

from flask_wtf import FlaskForm
from wtforms.fields import DateField, SelectField, StringField
from wtforms.validators import DataRequired, Optional

from services import expense_service


class ExpenseFilterForm(FlaskForm):
    class Meta:
        csrf = False

    from_date = DateField("From Date", validators=[Optional()], format="%Y-%m-%d")
    to_date = DateField(
        "To Date", validators=[Optional()], format="%Y-%m-%d", default=date.today()
    )
    category = SelectField("Category", validators=[Optional()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        category_choices = expense_service.get_expense_categories()
        category_choices = ["All"] + category_choices
        self.category.choices = category_choices
