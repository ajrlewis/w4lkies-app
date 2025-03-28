import datetime

from app import db


class Invoice(db.Model):
    invoice_id = db.Column(db.Integer, primary_key=True)

    date_start = db.Column(db.Date, nullable=False)
    date_end = db.Column(db.Date, nullable=False)
    date_issued = db.Column(db.Date, nullable=False)
    date_due = db.Column(db.Date, nullable=True)
    date_paid = db.Column(db.Date, nullable=True)

    price_subtotal = db.Column(db.Float, nullable=False)
    price_discount = db.Column(db.Float, nullable=False)
    price_total = db.Column(db.Float, nullable=False)

    bookings = db.relationship("Booking", backref="invoice")

    customer_id = db.Column(
        db.Integer, db.ForeignKey("customer.customer_id"), nullable=True
    )
    customer = db.relationship("Customer", backref="invoice")

    reference = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=True)
