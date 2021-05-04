from flask_login.utils import login_required
from . import delivery, role_name
from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, current_user
from app.models import *
from app.decorators import check_role
from app.utility import generate_random_password


@delivery.route('/logout', methods=["GET", "POST"], endpoint="logout")
@login_required
@check_role(role_name)
def logout():
	logout_user() 
	return redirect(url_for('delivery.login'))


@delivery.route("/", methods=["GET","POST"], endpoint="login")
def login():
	if request.method=="POST":
		email = request.form.get('email')
		password = request.form.get('password')
		user_obj = User.query.filter_by(email=email).first()
		if user_obj and user_obj.check_password(password) and "Delivery" in  user_obj.get_roles():
			login_user(user_obj)
			return redirect(url_for("delivery.dashboard"))
		else:
			flash("Invalid Email or Password", "danger")
			return redirect(url_for("delivery.login"))
	return render_template("delivery_index.html")

@delivery.route("/dashboard", methods=["GET"], endpoint="dashboard")
@login_required
@check_role("Delivery")
def dashboard():
	current_assigned_tender = current_user.pickups.filter(TenderPickup.status!="Delivered").first()
	past_tenders = current_user.pickups.filter_by(status="Delivered").all()
	# past_tenders = current_user.pickups.all()
	return render_template("delivery_dashboard.html", current_assigned_tender=current_assigned_tender,  past_tenders=past_tenders)



@delivery.route("/initiate_delivery", methods=["POST"], endpoint="initiate_delivery")
@login_required
@check_role(role_name)
def initiate_delivery():
	request_data = request.form
	if "tender_pickup_id" in request_data:
		tender_id = int(request_data["tender_pickup_id"])
		tender_obj = TenderPickup.query.get(tender_id)
		tender_obj.status = "Initiated"
		tender_obj.status_updated_on = datetime.now()
		db.session.commit()
		return jsonify({"status":"success"})
		
@delivery.route("/pickedup_delivery", methods=["POST"], endpoint="pickedup_delivery")
@login_required
@check_role(role_name)
def pickedup_delivery():
	request_data = request.form
	if "tender_pickup_id" in request_data:
		tender_id = int(request_data["tender_pickup_id"])
		tender_obj = TenderPickup.query.get(tender_id)
		tender_obj.status = "Picked Up"
		tender_obj.status_updated_on = datetime.now()
		db.session.commit()
		return jsonify({"status":"success"})


@delivery.route("/delivered", methods=["POST"], endpoint="delivered")
@login_required
@check_role(role_name)
def delivered():
	request_data = request.form
	if "tender_pickup_id" in request_data:
		tender_id = int(request_data["tender_pickup_id"])
		tender_obj = TenderPickup.query.get(tender_id)
		tender_obj.status = "Delivered"
		tender_obj.status_updated_on = datetime.now()
		db.session.commit()
		return jsonify({"status":"success"})
