from datetime import date

from flask_wtf import FlaskForm
from wtforms import DateField, SelectField
from wtforms.validators import DataRequired

from services import customer_service


class InvoiceGenerateForm(FlaskForm):
    customer_id = SelectField("Customer", coerce=int, validators=[DataRequired()])

    date_start = DateField(
        "Start Date",
        validators=[DataRequired()],
        format="%Y-%m-%d",
    )

    date_end = DateField(
        "End Date", validators=[DataRequired()], format="%Y-%m-%d", default=date.today()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        customer_id_choices = [
            (customer.customer_id, customer.name)
            for customer in customer_service.get_customers(is_active=True)
        ]
        self.customer_id.choices = customer_id_choices
