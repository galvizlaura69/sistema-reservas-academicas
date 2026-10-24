from flask import Blueprint

bp = __import__('app.spaces', fromlist=['bp']).bp


@bp.route('/')
def index():
    return 'spaces'
