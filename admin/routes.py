from . import admin
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user
from app.models import *

@admin.route("/login", methods=["GET","POST"], endpoint="login")
def login():
    if request.method=="POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user_obj = User.query.filter_by(email=email).first()
        if user_obj and user_obj.check_password(password) and "Admin" in  user_obj.get_roles():
            login_user(user_obj)
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid Email or Password", "danger")
            return redirect(url_for("admin.login"))

    return render_template("login.html")


@admin.route("/dashboard", methods=["GET"], endpoint="dashboard")
def dashboard():
    return render_template("dashboard.html")
