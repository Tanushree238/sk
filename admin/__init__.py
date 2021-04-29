from flask import Blueprint

admin = Blueprint("admin", __name__, url_prefix='/admin')

# / admin_login 
# /dashboard Welcome 
# sidenav - Delivery Person(CRUD) | Merchants(View all & Disable) | Tender ( Requests(Approve/ Reject) | Approved(Assign/ Track/ Recieved/ Return-Complete) | Completed )
