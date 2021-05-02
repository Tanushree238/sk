from flask import Blueprint

delivery = Blueprint("delivery", __name__, url_prefix='/delivery', template_folder="templates", static_folder="static")

role_name = "Delivery"

from delivery import routes