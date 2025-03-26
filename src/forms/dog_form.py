from datetime import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    BooleanField,
    DateField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Optional

from services import customer_service, vet_service


class DogForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired()],
        render_kw={"placeholder": "Scooby Doo"},
    )

    image = FileField(
        "Image",
        validators=[FileAllowed(["jpg", "jpeg", "png"], "Images only!")],
    )

    date_of_birth = DateField(
        "Date of Birth",
        validators=[Optional()],
        render_kw={"placeholder": "YYYY-MM-DD"},
    )

    breed = StringField(
        "Breed",
        render_kw={"placeholder": "Enter the breed of the dog"},
        validators=[Optional()],
    )

    is_allowed_treats = BooleanField("Allowed Treats", default=False)

    is_allowed_off_the_lead = BooleanField("Allowed Off the Lead", default=False)

    is_allowed_on_social_media = BooleanField("Allowed on Social Media", default=False)

    is_neutered_or_spayed = BooleanField("Neutered/Spayed", default=False)

    behavioral_issues = TextAreaField(
        "Behavioral Issues",
        validators=[Optional()],
        render_kw={
            "placeholder": "Separation anxiety, aggression, etc.",
        },
    )

    medical_needs = TextAreaField(
        "Medical Needs",
        validators=[Optional()],
        render_kw={
            "placeholder": "Allergies, medications, etc.",
        },
    )

    customer_id = SelectField("Customer", validators=[DataRequired()], coerce=int)
    vet_id = SelectField("Vet", validators=[DataRequired()], coerce=int)

    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        customers = customer_service.get_customers(is_active=True)
        customer_id_choices = [
            (customer.customer_id, customer.name) for customer in customers
        ]
        self.customer_id.choices = customer_id_choices

        vets = vet_service.get_vets()
        vet_id_choices = [(vet.vet_id, vet.name) for vet in vets]
        self.vet_id.choices = vet_id_choices
