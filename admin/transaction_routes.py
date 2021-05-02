from flask_login.utils import login_required
from sqlalchemy.sql.functions import user
from . import admin, role_name
from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user
from app.models import *
from app.decorators import check_role
from sqlalchemy import or_


@admin.route("/transaction/add/<int:tender_id>", methods=["GET", "POST"], endpoint="add_transaction")
@login_required
@check_role(role_name)
def add_transaction(tender_id, next_url=None):
    tender = Tender.query.get(tender_id)
    if request.method=="POST":
        data = request.form.to_dict()
        if tender.status=="Approved" or tender.status=="Recieved":
            transaction_type = "D"
        elif tender.status=="Returned":
            transaction_type = "C"

        if "gst_percentage" in data:
            gst_percentage = data["gst_percentage"]
        else:
            gst_percentage = None

        transaction_obj = Transactions(
                                    tender_id = tender_id, 
                                    transaction_type = transaction_type, 
                                    amount = int(data["amount"]), 
                                    mode = data["payment_mode"], 
                                    mode_description = data["payment_mode_description"], 
                                    payment_date = datetime.strptime(data["payment_date"], "%Y-%m-%d"), 
                                    description = data["description"], 
                                    gst_percentage = gst_percentage, 
                        )
        db.session.add(transaction_obj)

        if transaction_type == "D":
            tender.paid_amount += int(data["amount"])
        elif transaction_type == "C":
            tender.paid_amount -= int(data["amount"])

        if tender.paid_amount==tender.total_amount:
            tender.status = "Completed"
            tender.status_updated_on = datetime.now()

        db.session.commit()
        flash("Transaction added successfully", "success")
        if next_url:
            return redirect(next_url)
        else:
            return redirect(url_for('admin.merchant_tenders', merchant_id=tender.user.id))

    return render_template('transaction/add.html', tender=tender, next_url=next_url)