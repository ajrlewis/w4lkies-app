from datetime import date

from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, SelectField, StringField
from wtforms.validators import DataRequired, Optional

from services import customer_service


class InvoiceForm(FlaskForm):
    date_start = DateField(
        "Start Date",
        validators=[DataRequired()],
        format="%Y-%m-%d",
    )

    date_end = DateField(
        "End Date", validators=[DataRequired()], format="%Y-%m-%d", default=date.today()
    )

    date_issued = DateField(
        "Date Issued",
        validators=[DataRequired()],
        format="%Y-%m-%d",
        default=date.today(),
    )

    date_paid = DateField("Date Paid", validators=[Optional()], format="%Y-%m-%d")

    price_subtotal = DecimalField(
        "Subtotal Price / £",
        validators=[DataRequired()],
        render_kw={"placeholder": "The sub total price of the invoice"},
    )

    price_discount = DecimalField(
        "Total Discount Price / £",
        validators=[DataRequired()],
        render_kw={"placeholder": "The sub total price of the invoice"},
    )

    price_total = DecimalField(
        "Total Price / £",
        validators=[DataRequired()],
        render_kw={"placeholder": "The total price of the invoice"},
    )

    customer_id = SelectField("Customer", coerce=int, validators=[DataRequired()])

    reference = StringField(
        "Reference",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter the reference of the invoice"},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        customer_id_choices = [
            (customer.customer_id, customer.name)
            for customer in customer_service.get_customers(is_active=True)
        ]
        self.customer_id.choices = customer_id_choices
