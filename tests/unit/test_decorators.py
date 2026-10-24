from flask_login import login_user, logout_user
from app.models.user import User
from app.services.auth_service import AuthService
from app.utils.decorators import role_required


def test_role_required_denies_solicitante(app):
    with app.app_context():
        u = AuthService.register('A', 'e@e.com', 'pass')
        @role_required('administrador')
        def admin_only():
            return 'ok'
        # simulate
        from flask import Flask
        with app.test_request_context():
            login_user(u)
            try:
                admin_only()
                assert False, 'should abort'
            except Exception as ex:
                from werkzeug.exceptions import Forbidden
                assert isinstance(ex, Forbidden)
            finally:
                logout_user()
