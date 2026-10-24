from flask import Blueprint

bp = __import__('app.reservations', fromlist=['bp']).bp


@bp.route('/')
def index():
    return 'reservations'
