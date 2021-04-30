from flask import Blueprint

merchant = Blueprint("merchant", __name__, url_prefix='/merchant', template_folder='templates')

from merchant import routes