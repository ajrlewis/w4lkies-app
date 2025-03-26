import datetime

from app import db


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    emergency_contact_name = db.Column(db.String(255), nullable=False)
    emergency_contact_phone = db.Column(db.String(20), nullable=False)
    signed_up_on = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    dogs = db.relationship("Dog", backref="customer", lazy=True)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=True)
