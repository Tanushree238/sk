from flask_login.utils import login_required
from . import admin, role_name
from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user
from app.models import *
from app.decorators import check_role
from app.utility import generate_random_password

@admin.route("/delivery_person", methods=["GET", "POST"], endpoint="delivery_person")
@login_required
@check_role("Admin")
def delivery_person():
	delivery_persons = DeliveryPersonDetails.query.order_by( DeliveryPersonDetails.id.desc() ).all()
	return render_template('delivery_person/home.html', delivery_persons=delivery_persons)

@admin.route("/add_delivery_person", methods=["GET", "POST"], endpoint="add_delivery_person")
@login_required
@check_role("Admin")
def add_delivery_person():
	if request.method=="POST":
		data = request.form.to_dict()
		user_obj = User(
			name=data["name"],
			contact=data["contact"],
			email=data["email"]
		)

		random_password = generate_random_password()
		user_obj.set_password(random_password)
		with open("delivery_person_passwords.txt", "a") as f:
			f.write("{} : {}\n".format(user_obj.email, random_password))

		db.session.add(user_obj)
		db.session.commit()

		delivery_person_role = Role.query.filter_by(name="delivery").first()
		if not delivery_person_role:
			delivery_person_role = Role(name="delivery")
			db.session.add(delivery_person_role)
			db.session.commit()

		ur = UserRole(
			user_id=user_obj.id,
			role_id=delivery_person_role.id
		)
		db.session.add(ur)

		dpd_obj = DeliveryPersonDetails(
			user_id=user_obj.id,
			address=data["address"],
			city=data["city"],
			state=data["state"],
			pin_code=data["pincode"],
			aadhar_number=data["aadhar_number"]
		)

		db.session.add(dpd_obj)
		db.session.commit()

		flash("Delivery Person {} successfully registered".format(user_obj.name), "success")
		return redirect(url_for("admin.add_delivery_person"))

	return render_template('delivery_person/add.html')
	
@admin.route("/edit_delivery_person/<int:delivery_person_id>", methods=["GET", "POST"], endpoint="edit_delivery_person")
@login_required
@check_role("Admin")
def edit_delivery_person(delivery_person_id):
	delivery_person = DeliveryPersonDetails.query.get(delivery_person_id)
	user = delivery_person.user
	if request.method=="POST":
		data = request.form.to_dict()
		user_obj = User.query.get(data["user_id"])
		user_obj.name=data["name"]
		user_obj.contact=data["contact"]
		user_obj.email=data["email"]
		db.session.commit()

		dpd_obj = DeliveryPersonDetails.query.get(data["delivery_person_id"])

		dpd_obj.address=data["address"]
		dpd_obj.city=data["city"]
		dpd_obj.state=data["state"]
		dpd_obj.pin_code=data["pincode"]
		dpd_obj.aadhar_number=data["aadhar_number"]
		db.session.commit()

		flash("Delivery Person data updated successfully", "success")
		return redirect(url_for("admin.edit_delivery_person", delivery_person_id=data["delivery_person_id"]))

	return render_template('delivery_person/edit.html', delivery_person=delivery_person, user=user)

@admin.route("/delete_delivery_person", methods=["POST"], endpoint="delete_delivery_person")
@login_required
@check_role("Admin")
def delete_delivery_person():
	delivery_person_id = int(request.form.get("delivery_person_id"))
	user = DeliveryPersonDetails.query.get(delivery_person_id).user
	flash("Delivery Person {} removed successfully".format(user.name), "success")
	db.session.delete(user)
	db.session.commit()
	return jsonify({"status": True})
