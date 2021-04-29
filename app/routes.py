from app import app, db
from flask import redirect,render_template,url_for, jsonify, request,flash,session
from app.models import *
from flask_login import login_user, logout_user


@app.route('/', methods=["GET","POST"])
def login():
    if request.method == "POST":
        request_data = request.form
        user_obj = User.query.filter_by(email=request_data["email"]).first()
        if user_obj and user_obj.check_password( request_data["password"]) and "Merchant" in user_obj.get_roles():
            login_user(user_obj)
            return redirect( url_for("merchant.dashboard") )
        else:
            flash("Invalid Email or Password.", "danger")
            return redirect("login")
    return render_template("index.html")


@app.route('/register/', methods=["GET","POST"])
def register():
    if request.method == "POST":
        request_data = request.form 
        user_obj = User(
            name = request_data["name"],
            email = request_data["email"],
            contact = request_data["contact"]
            )
        user_obj.set_password(request_data["password"])
        db.session.add(user_obj)
        db.session.commit()
        role_obj = Role.query.filter_by(name="Merchant").first()
        if not role_obj:
            role_obj = Role(name="Merchant")
            db.session.add(role_obj)
            db.session.commit()
        user_role_obj = UserRole(user_id=user_obj.id, role_id=role_obj.id)
        db.session.add(user_role_obj)
        db.session.commit()
        return redirect( url_for('login') )
    return render_template("register.html")


