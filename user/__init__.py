from flask import Blueprint

user = Blueprint("user", __name__, url_prefix='/user', template_folder="templates", static_folder="static")

role_name = "User"

from user import routes