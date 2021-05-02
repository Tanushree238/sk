from flask_login.utils import login_required
from sqlalchemy.sql.functions import user
from . import admin, role_name
from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user
from app.models import *
from app.decorators import check_role


@admin.route("/tender/requests", methods=["GET", "POST"], endpoint="tender_requests")
@login_required
@check_role(role_name)
def tender_requests():
    tenders = Tender.query.filter( Tender.status=="Requested"  ).order_by( Tender.created_on.desc() ).all()
    tenders = list(enumerate(tenders,1))
    return render_template("tenders/request.html", tenders=tenders)

@admin.route("/tender/approved", methods=["GET", "POST"], endpoint="tender_approved")
@login_required
@check_role(role_name)
def tender_approved():
    tenders = Tender.query.filter( Tender.status!="Requested", Tender.status!="Drafted" ).order_by( Tender.created_on.desc() ).all()
    tenders = list(enumerate(tenders,1))
    return render_template("tenders/approved.html", tenders=tenders)