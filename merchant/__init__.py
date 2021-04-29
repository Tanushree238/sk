from flask import Blueprint

merchant = Blueprint("merchant", __name__, url_prefix='/merchant')

from . import routes