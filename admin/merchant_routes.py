from flask_login.utils import login_required
from sqlalchemy.sql.functions import user
from . import admin, role_name
from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user
from app.models import *
from app.decorators import check_role


@admin.route("/merchant", methods=["GET", "POST"], endpoint="merchant")
@login_required
@check_role(role_name)
def merchant():
    merchants = MerchantCompanyDetails.query.order_by( MerchantCompanyDetails.id.desc() ).all()
    return render_template("merchant/home.html", merchants=merchants)


@admin.route("/merchant_tenders/<int:merchant_id>", methods=["GET", "POST"], endpoint="merchant_tenders")
@login_required
@check_role(role_name)
def merchant_tenders(merchant_id):
    tenders = Tender.query.filter( Tender.merchant_id==merchant_id, Tender.status!="Drafted"  ).order_by( Tender.created_on.desc() ).all()
    tenders = list(enumerate(tenders,1))
    return render_template("merchant/tenders.html", tenders=tenders)


@admin.route("/approve_tender", methods=["POST"], endpoint="approve_tender")
@login_required
@check_role(role_name)
def approve_tender():
    tender_id = int(request.form.get("tender_id"))
    tender = Tender.query.get(tender_id)
    tender.status = "Approved"
    tender.status_updated_on = datetime.now()
    db.session.commit()
    if tender.advance_amount>0:
        flash("Tender has been Approved successfully", "success")
        flash("Please Make an Transaction for Advance Payment of ₹{}".format(tender.advance_amount), "info")
    else:
        flash("Tender has been Approved successfully", "success")

    return jsonify({"status": "success"})


@admin.route("/reject_tender", methods=["POST"], endpoint="reject_tender")
@login_required
@check_role(role_name)
def reject_tender():
    tender_id = int(request.form.get("tender_id"))
    tender = Tender.query.get(tender_id)
    tender.status = "Rejected"
    tender.status_updated_on = datetime.now()
    db.session.commit()
    flash("Tender has been Rejected successfully", "success")

    return jsonify({"status": "success"})


@admin.route("/fetch_delivery_persons", methods=["GET"], endpoint="fetch_delivery_persons")
@login_required
@check_role(role_name)
def fetch_delivery_persons():
    delivery_persons = db.session.query( DeliveryPersonDetails.id, User.name ).join(User, User.id==DeliveryPersonDetails.user_id).filter( DeliveryPersonDetails.status=="Available" ).all()
    delivery_persons = list(map(lambda x: dict(x), delivery_persons))
    return jsonify(delivery_persons)


@admin.route("/assign_delivery_persons", methods=["POST"], endpoint="assign_delivery_persons")
@login_required
@check_role(role_name)
def assign_delivery_persons():
    delivery_person_id = int(request.form.get("delivery_person_id"))
    tender_id = int(request.form.get("tender_id"))
    delivery_person = DeliveryPersonDetails.query.get(delivery_person_id)
    user = delivery_person.user
    tender = Tender.query.get(tender_id)

    delivery_person.status = "Uavailable"
    tender.status = "Assigned"
    tender.status_updated_on = datetime.now()
    pickup_obj = TenderPickup(delivery_person_id=user.id, tender_id=tender_id)
    db.session.add(pickup_obj)
    db.session.commit()
    
    flash("Tender Pickup Assigned to {}".format(user.name), "success")
    return redirect(url_for('admin.merchant_tenders', merchant_id=tender.user.id))


@admin.route("/received_delivery", methods=["POST"], endpoint="received_delivery")
@login_required
@check_role(role_name)
def received_delivery():
    tender_id = int(request.form.get("tender_id"))
    tender = Tender.query.get(tender_id)
    delivery_person = tender.pickup.first().user.delivery_persons.first()
    tender.status = "Recieved"
    delivery_person.status = "Available"

    tender.status_updated_on = datetime.now()
    db.session.commit()
    flash("Tender has been received successfully", "success")
    flash("Please Make a Transaction for remaining payment of ₹{}".format(tender.total_amount-tender.paid_amount), "info")

    return jsonify({"status": "success"})


