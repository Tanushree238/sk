from app import app, db
from flask import redirect,render_template,url_for, jsonify, request,flash,session
from app.models import *

@app.route('/')
def login():
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


