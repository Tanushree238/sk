from flask_login.utils import login_required
from . import admin, role_name
from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user
from app.models import *
from app.decorators import check_role
from app.utility import generate_random_password

@admin.route("/", methods=["GET","POST"], endpoint="login")
def login():
	if request.method=="POST":
		email = request.form.get('email')
		password = request.form.get('password')
		print(email, password)
		user_obj = User.query.filter_by(email=email).first()
		print(user_obj)
		if user_obj and user_obj.check_password(password) and "Admin" in  user_obj.get_roles():
			login_user(user_obj)
			return redirect(url_for("admin.dashboard"))
		else:
			flash("Invalid Email or Password", "danger")
			return redirect(url_for("admin.login"))

	return render_template("login.html")

@admin.route("/dashboard", methods=["GET"], endpoint="dashboard")
@login_required
@check_role("Admin")
def dashboard():
	return render_template("dashboard.html")

@admin.route("/validate_email", methods=["POST"], endpoint="validate_email")
@login_required
@check_role("Admin")
def validate_email():
	email = request.form.get("email")
	user_id = request.form.get("user_id")
	print(email, user_id)
	if email:
		user = User.query.filter_by(email=email).first()
		if not user or ( user_id and user.id==int(user_id) ):
			return 'true'
		else:
			return 'false'

@admin.route('/logout', endpoint="logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for("admin.login"))
