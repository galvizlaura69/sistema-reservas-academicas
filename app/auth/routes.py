from flask import Blueprint, render_template

bp = __import__('app.auth', fromlist=['bp']).bp


@bp.route('/login')
def login():
    return 'login'
