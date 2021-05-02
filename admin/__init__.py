from flask import Blueprint

admin = Blueprint("admin", __name__, url_prefix='/admin', template_folder="templates", static_folder="static")

# / admin_login 
# /dashboard Welcome 
# sidenav - Delivery Person(CRUD) | Merchants(View all & Disable) | Tender ( Requests(Approve/ Reject) | Approved(Assign/ Track/ Recieved/ Return-Complete) | Completed )

role_name = "Admin"

from . import routes, delivery_person_routes, merchant_routes, tender_routes, transaction_routes