from flask import Blueprint

bp = Blueprint('spaces', __name__, url_prefix='/spaces')

from app.spaces import routes  # noqa
