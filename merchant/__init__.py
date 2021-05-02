from flask import Blueprint

merchant = Blueprint("merchant", __name__, url_prefix='/merchant', template_folder='templates', static_folder="static")

from merchant import routes