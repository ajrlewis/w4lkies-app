import datetime

from app import db


class Booking(db.Model):
    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    customer_id = db.Column(
        db.Integer, db.ForeignKey("customer.customer_id"), nullable=False
    )
    customer = db.relationship("Customer", backref="booking")

    service_id = db.Column(
        db.Integer, db.ForeignKey("service.service_id"), nullable=False
    )
    service = db.relationship("Service", backref="booking")

    invoice_id = db.Column(
        db.Integer, db.ForeignKey("invoice.invoice_id"), nullable=True
    )

    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=True)
    user = db.relationship("User", backref="booking", foreign_keys=[user_id])

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=True)
