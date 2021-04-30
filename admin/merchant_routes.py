from flask_login.utils import login_required
from . import admin, role_name
from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user
from app.models import *
from app.decorators import check_role


@admin.route("/merchant", methods=["GET", "POST"], endpoint="merchant")
@login_required
@check_role("Admin")
def merchant():
    merchants = MerchantCompanyDetails.query.order_by( MerchantCompanyDetails.id.desc() ).all()
    return render_template("merchant/home.html", merchants=merchants)