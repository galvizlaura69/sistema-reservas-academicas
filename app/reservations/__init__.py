from flask import Blueprint

bp = Blueprint('reservations', __name__, url_prefix='/reservations')

from app.reservations import routes  # noqa
