from flask import render_template

bp = __import__('app.admin', fromlist=['bp']).bp


@bp.route('/')
def index():
    return render_template('admin/index.html')
