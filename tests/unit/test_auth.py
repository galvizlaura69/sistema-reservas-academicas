from app.models.user import User
from app.services.auth_service import AuthService


def test_register_solicitante_default(app):
    with app.app_context():
        user = AuthService.register('Test', 'test@example.com', 'pass123')
        assert user.role == 'solicitante'
        assert user.check_password('pass123')


def test_authenticate_success(app):
    with app.app_context():
        AuthService.register('Test', 'test2@example.com', 'pass123')
        user = AuthService.authenticate('test2@example.com', 'pass123')
        assert user is not None


def test_authenticate_fail(app):
    with app.app_context():
        AuthService.register('Test', 'test3@example.com', 'pass123')
        user = AuthService.authenticate('test3@example.com', 'wrong')
        assert user is None
