from flask import render_template

bp = __import__('app.spaces', fromlist=['bp']).bp


@bp.route('/')
def index():
    return render_template('spaces/index.html')
