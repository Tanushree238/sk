from flask_login.utils import login_required
from . import user, role_name
from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, current_user
from app.models import *
from app.decorators import check_role
from app.utility import generate_random_password
from .ml_model import *
from sqlalchemy import or_

@user.route('/logout', methods=["GET", "POST"], endpoint="logout")
@login_required
@check_role(role_name)
def logout():
	logout_user() 
	return redirect(url_for('login'))


@user.route("/dashboard", methods=["GET"], endpoint="dashboard")
@login_required
@check_role(role_name)
def dashboard():
	popular_product_categories = fetch_popular_product_categories().head()
	popular_categories = []
	for item in popular_product_categories.iterrows():
		category_obj = ProductCategory.query.get(item[0])
		popular_categories.append(category_obj)
	return render_template("user_dashboard.html", popular_categories = popular_categories, len = len)


@user.route("/search", methods=["POST"], endpoint="product_search")
@login_required
@check_role(role_name)
def product_search():
	request_data = request.form	
	recommended_cluster = fetch_recommended_cluster(request_data['search_text'])
	search_results = []
	for i in range(10):
		search_results+=Product.query.filter(Product.name.like('%{}%'.format(recommended_cluster[i]))).order_by(Product.rating.desc()).limit(10).all()
	results = search_results
	return render_template("search_results.html", results = results,searched_text = request_data['search_text'],  len = len)

