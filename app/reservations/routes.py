from flask import render_template

bp = __import__('app.reservations', fromlist=['bp']).bp


@bp.route('/')
def index():
    return render_template('reservations/index.html')
