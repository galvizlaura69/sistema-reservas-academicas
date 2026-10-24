from app.services.auth_service import AuthService
from app.services.user_service import UserService


def test_list_users_filters(app):
    with app.app_context():
        AuthService.register('A', 'a@a.com', 'pass')
        AuthService.register('B', 'b@b.com', 'pass', role='administrador')
        users = UserService.list_users(role='administrador')
        assert len(users) == 1
        assert users[0].email == 'b@b.com'


def test_set_role(app):
    with app.app_context():
        u = AuthService.register('A', 'c@c.com', 'pass')
        UserService.set_role(u.id, 'administrador')
        from app.models.user import User
        u2 = User.query.get(u.id)
        assert u2.role == 'administrador'


def test_set_active(app):
    with app.app_context():
        u = AuthService.register('A', 'd@d.com', 'pass')
        UserService.set_active(u.id, False)
        from app.models.user import User
        u2 = User.query.get(u.id)
        assert u2.active is False
