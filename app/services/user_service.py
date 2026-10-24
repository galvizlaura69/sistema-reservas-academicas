from app import db
from app.models.user import User


class UserService:
    @staticmethod
    def list_users(role=None, active=None):
        query = User.query
        if role:
            query = query.filter_by(role=role)
        if active is not None:
            query = query.filter_by(active=active)
        return query.all()

    @staticmethod
    def set_role(user_id, role):
        user = User.query.get_or_404(user_id)
        if role not in ['administrador', 'solicitante']:
            raise ValueError('invalid_role')
        user.role = role
        db.session.commit()
        return user

    @staticmethod
    def set_active(user_id, active):
        user = User.query.get_or_404(user_id)
        user.active = bool(active)
        db.session.commit()
        return user
