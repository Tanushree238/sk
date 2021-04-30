from flask import redirect,render_template,url_for, jsonify, request,flash,session
from merchant import merchant
from flask_login import login_required, current_user, logout_user
from app.decorators import *
from app.models import *


role_name = "Merchant"


@merchant.route('/logout', methods=["GET", "POST"], endpoint="logout")
@login_required
@check_role(role_name)
def logout():
	logout_user()
	return redirect(url_for('login'))


@merchant.route('/', methods=["GET", "POST"], endpoint="dashboard")
@login_required
@check_role(role_name)
def dashboard():
	if request.method == "GET":
		merchant_details_obj=MerchantCompanyDetails.query.filter_by(user_id=current_user.id).first()
		if merchant_details_obj:
			return redirect( url_for("merchant.merchant_home") )
	if request.method == "POST":
		request_data = request.form
		merchant_details_obj = MerchantCompanyDetails(
			user_id = current_user.id,
			name = request_data["name"],
			address= request_data["address"],
			city= request_data["city"],
			state= request_data["state"],
			pin_code= request_data["pin_code"],
			gst_number = request_data["gst_number"],
			aadhar_number = request_data["aadhar_number"]
		)
		db.session.add(merchant_details_obj)
		db.session.commit()
		flash("Your Profile Details have been added successfully. You can start selling.", "success")
		return redirect( url_for("merchant.merchant_home") )
	return render_template("merchant_details.html")


@merchant.route('/dashboard', methods=["GET"], endpoint="merchant_home")
@login_required
@check_role(role_name)
def merchant_home():
	return render_template("merchant_dashboard.html")


@merchant.route('/tender_drafts', methods=["GET", "POST"], endpoint="drafts")
@login_required
@check_role(role_name)
def drafts():
	tender_drafts = Tender.query.filter_by(merchant_id=current_user.id, status="Drafted").all()
	tender_drafts = list(enumerate(tender_drafts,1))
	product_categories = db.session.query(ProductCategory.id, ProductCategory.name).all()
	if request.method == "POST":
		request_data =  request.form
		print(request_data)
		tender_obj = Tender(
			merchant_id = current_user.id,
			advance_amount = request_data["advance_amount"],
			paid_amount = 0,
			status_updated_on = datetime.now(),
		)
		db.session.add(tender_obj)
		db.session.commit()
		total_amount = 0
		for i in range(int(request_data["product_count"])):
			id, price = map(int,request_data['product_name_'+str(i+1)].split("|"))
			quantity = int(request_data["product_quantity_"+str(i+1)])
			tender_product_obj = TenderProductMapper(
				tender_id = tender_obj.id,
				product_id = id,
				quantity = quantity,
				total_amount =  quantity * price
			)
			db.session.add(tender_product_obj)
			db.session.commit()
			total_amount += tender_product_obj.total_amount
		tender_obj.total_amount = total_amount
		db.session.commit()
		return redirect( url_for('merchant.drafts') )
	return render_template("drafts.html", tender_drafts=tender_drafts, product_categories=product_categories)



@merchant.route("/fetch_products", methods=["POST"], endpoint="fetch_products")
@login_required
@check_role(role_name)
def fetch_products():
	request_data = request.form
	if "category" in request_data:
		category_id = int(request_data["category"])
		product_list = db.session.query(Product.id, Product.marked_retail_price, Product.name).filter(Product.category_id==category_id).all()
		product_data = []
		for prod in product_list:
			product = {}
			product['id']=prod[0]
			product['name']=prod[2]
			product['price']=prod[1]
			product_data.append(product)

		return jsonify({"product_list":product_data})


@merchant.route("/delete_tender", methods=["POST"], endpoint="delete_tender")
@login_required
@check_role(role_name)
def delete_tender():
	request_data = request.form
	if "tender_id" in request_data:
		tender_id = int(request_data["tender_id"])
		tender_obj = Tender.query.get(tender_id)
		db.session.delete(tender_obj)
		db.session.commit()
		return jsonify({"status":"success"})


@merchant.route("/request_tender", methods=["POST"], endpoint="request_tender")
@login_required
@check_role(role_name)
def request_tender():
	request_data = request.form
	if "tender_id" in request_data:
		tender_id = int(request_data["tender_id"])
		tender_obj = Tender.query.get(tender_id)
		tender_obj.status = "Requested"
		tender_obj.status_updated_on = datetime.now()
		db.session.commit()
		return jsonify({"status":"success"})


@merchant.route('/tender_requests', methods=["GET", "POST"], endpoint="requests")
@login_required
@check_role(role_name)
def requests():
	tender_requests = Tender.query.filter_by(merchant_id=current_user.id, status="Requested").all()
	tender_requests = list(enumerate(tender_requests,1))
	return render_template("requests.html", tender_requests=tender_requests)


@merchant.route('/tenders', methods=["GET", "POST"], endpoint="tenders")
@login_required
@check_role(role_name)
def tenders():
	tenders = Tender.query.filter_by(merchant_id=current_user.id).all()
	tenders = list(enumerate(tenders,1))
	return render_template("tenders.html", tenders=tenders)