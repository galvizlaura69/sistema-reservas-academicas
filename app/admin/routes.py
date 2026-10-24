from flask import Blueprint

bp = __import__('app.admin', fromlist=['bp']).bp


@bp.route('/')
def index():
    return 'admin'
