from datetime import datetime
from app import db


class Space(db.Model):
    __tablename__ = 'spaces'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(30), nullable=False)
    capacity = db.Column(db.Integer)
    location = db.Column(db.String(120))
    status = db.Column(db.String(20), nullable=False, default='activo')
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reservations = db.relationship('Reservation', backref='space', lazy=True)

    def is_active(self):
        return self.status == 'activo'
