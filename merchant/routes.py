from flask import redirect,render_template,url_for, jsonify, request,flash,session
from merchant import merchant

@merchant.route('/', methods=["GET"], endpoint="dashboard")
def dashboard():
    return "HELLO MERCHANT"
