import datetime

from app import db


class Invoice(db.Model):
    invoice_id = db.Column(db.Integer, primary_key=True)

    number = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    date_issued = db.Column(db.Date, nullable=False)
    # date_paid = db.Column(db.Date, nullable=True)
    is_paid = db.Column(db.Boolean, nullable=False, default=False)
    subtotal_price = db.Column(db.Float, nullable=False)
    total_price_discount = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    bookings = db.relationship("Booking", backref="invoice")

    customer_id = db.Column(
        db.Integer, db.ForeignKey("customer.customer_id"), nullable=True
    )
    customer = db.relationship("Customer", backref="invoice")

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=True)
