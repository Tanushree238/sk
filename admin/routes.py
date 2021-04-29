from . import admin
from flask import render_template, redirect, url_for, request



@admin.route("/login", methods=["GET","POST"], endpoint="login")
def login():
    if request.method=="POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        print(username, password)
    return render_template("login.html")


@admin.route("/dashboard", methods=["GET"], endpoint="dashboard")
def dashboard():
    return render_template("dashboard.html")
