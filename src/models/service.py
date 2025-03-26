import datetime

from app import db


class Service(db.Model):
    service_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), default="", nullable=False)
    duration = db.Column(db.Float, nullable=True)
    is_publicly_offered = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=True)
