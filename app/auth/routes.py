from flask import render_template

bp = __import__('app.auth', fromlist=['bp']).bp


@bp.route('/login')
def login():
    return render_template('auth/login.html')
