from datetime import datetime
from app import db


class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    space_id = db.Column(db.Integer, db.ForeignKey('spaces.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pendiente')
    reason = db.Column(db.Text)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    decision_at = db.Column(db.DateTime)
    cancelled_at = db.Column(db.DateTime)
    cancelled_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    cancel_reason = db.Column(db.Text)
    has_conflict = db.Column(db.Boolean, default=False)
    conflict_note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    admin = db.relationship('User', foreign_keys=[admin_id], backref='decided_reservations')
    cancelled_by = db.relationship('User', foreign_keys=[cancelled_by_id], backref='cancelled_reservations')
