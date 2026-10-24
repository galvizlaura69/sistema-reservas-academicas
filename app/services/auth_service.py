from app import db
from app.models.user import User


class AuthService:
    @staticmethod
    def register(name, email, password, role='solicitante'):
        if User.query.filter_by(email=email).first():
            raise ValueError('email_exists')
        user = User(name=name, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def authenticate(email, password):
        user = User.query.filter_by(email=email).first()
        if not user or not user.active:
            return None
        if user.check_password(password):
            return user
        return None
