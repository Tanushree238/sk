from app import db, login_manager
from sqlalchemy.orm import backref
from datetime import datetime
from time import time
from flask import url_for
from time import time
import os
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func,text
from flask_login import UserMixin

class User(db.Model, UserMixin):

	id = db.Column( db.Integer, primary_key=True )
	name = db.Column( db.String(100), nullable=False )
	contact = db.Column( db.BigInteger, unique=True, nullable=False)
	email = db.Column( db.String(40), nullable=False, unique=True )
	password = db.Column( db.String(255) )

	user_roles = db.relationship('UserRole', backref="user", lazy="dynamic", cascade="save-update, delete")
	delivery_persons = db.relationship('DeliveryPersonDetails', backref="user", lazy="dynamic", cascade="save-update, delete")
	merchants = db.relationship('MerchantCompanyDetails', backref="user", lazy="dynamic", cascade="save-update, delete")
	tenders = db.relationship('Tender', backref="user", lazy="dynamic", cascade="save-update, delete")
	pickups = db.relationship('TenderPickup', backref="user", lazy="dynamic", cascade="save-update, delete")

	created_on = db.Column( db.DateTime, default=datetime.now )
	updated_on = db.Column( db.DateTime, onupdate = datetime.now )

	def get_roles(self):
		roles = set()
		for user_role_obj in self.user_roles.all():
			roles.add(user_role_obj.role.name)
		return roles

	def set_password(self,password):
		self.password = generate_password_hash(password)

	def check_password( self,password ):
		return check_password_hash( self.password, password ) 

	def __repr__(self):
		return self.name

	
class Role(db.Model):

	id = db.Column( db.Integer, primary_key=True )
	name = db.Column( db.String(100), nullable=False )

	user_roles = db.relationship('UserRole', backref="role", lazy="dynamic", cascade="save-update, delete")

	created_on = db.Column( db.DateTime, default=datetime.now )
	updated_on = db.Column( db.DateTime, onupdate = datetime.now )
 
	def __repr__(self):
		return self.name


class UserRole(db.Model):

	id = db.Column( db.Integer, primary_key=True )
	user_id = db.Column( db.Integer, db.ForeignKey('user.id') )
	role_id = db.Column( db.Integer, db.ForeignKey('role.id') )

	created_on = db.Column( db.DateTime, default=datetime.now )
	updated_on = db.Column( db.DateTime, onupdate = datetime.now )


class MerchantCompanyDetails(db.Model):

	id = db.Column( db.Integer, primary_key=True )
	user_id = db.Column( db.Integer, db.ForeignKey('user.id') )
	name = db.Column( db.String(255), nullable=False )
	address = db.Column( db.String(255), nullable=False )
	city = db.Column( db.String(255), nullable=False )
	state = db.Column( db.String(255), nullable=False )
	pin_code = db.Column( db.String(6), nullable=False )
	gst_number = db.Column( db.BigInteger, unique=True, nullable=False)
	aadhar_number = db.Column( db.BigInteger, unique=True, nullable=False)

	created_on = db.Column( db.DateTime, default=datetime.now )
	updated_on = db.Column( db.DateTime, onupdate = datetime.now )


class DeliveryPersonDetails(db.Model):

	id = db.Column( db.Integer, primary_key=True )
	user_id = db.Column( db.Integer, db.ForeignKey('user.id') )
	address = db.Column( db.String(255), nullable=False )
	city = db.Column( db.String(255), nullable=False )
	state = db.Column( db.String(255), nullable=False )
	pin_code = db.Column( db.String(6), nullable=False )
	aadhar_number = db.Column( db.BigInteger, unique=True, nullable=False)
	status = db.Column( db.String(255), nullable=False , default="Available")

	created_on = db.Column( db.DateTime, default=datetime.now )
	updated_on = db.Column( db.DateTime, onupdate = datetime.now )


class ProductCategory(db.Model):

	id = db.Column( db.Integer, primary_key=True )
	name = db.Column( db.String(100), nullable=False )

	products = db.relationship('Product', backref="category", lazy="dynamic", cascade="save-update, delete")

	created_on = db.Column( db.DateTime, default=datetime.now )
	updated_on = db.Column( db.DateTime, onupdate = datetime.now )
 
	def __repr__(self):
		return self.name


class Product(db.Model):
	
	id = db.Column( db.Integer, primary_key=True )
	name = db.Column( db.String(255), nullable=False )
	marked_retail_price = db.Column( db.Integer )
	stock_quantity = db.Column( db.Integer )
	specifications = db.Column( db.Text )
	rating = db.Column( db.Float )
	image = db.Column( db.String(200))

	category_id = db.Column( db.Integer, db.ForeignKey('product_category.id') )

	tenders = db.relationship('TenderProductMapper', backref="product_obj", lazy="dynamic", cascade="save-update, delete")

	created_on = db.Column( db.DateTime, default=datetime.now )
	updated_on = db.Column( db.DateTime, onupdate = datetime.now )
 
	def __repr__(self):
		return self.name


class Tender(db.Model):

	id = db.Column( db.Integer, primary_key=True )
	merchant_id = db.Column( db.Integer, db.ForeignKey('user.id') )
	total_amount = db.Column(db.Integer)
	advance_amount = db.Column(db.Integer)
	paid_amount = db.Column(db.Integer)
	status = db.Column( db.String(200), nullable=False, default = "Drafted")
	# Drafted/Requested/Rejected/Approved/Assigned/Recieved/Completed/Returned
	status_updated_on = db.Column( db.DateTime)

	products = db.relationship('TenderProductMapper', backref="tender_obj", lazy="dynamic", cascade="save-update, delete")
	pickup = db.relationship('TenderPickup', backref="tender_obj", lazy="dynamic", cascade="save-update, delete")
	transactions = db.relationship('Transactions', backref="tender_obj", lazy="dynamic", cascade="save-update, delete")

	created_on = db.Column( db.DateTime, default=datetime.now )
	updated_on = db.Column( db.DateTime, onupdate = datetime.now )
  

class TenderProductMapper(db.Model):

	id = db.Column( db.Integer, primary_key=True )
	tender_id = db.Column( db.Integer, db.ForeignKey('tender.id') )
	product_id = db.Column( db.Integer, db.ForeignKey('product.id') )
	quantity = db.Column( db.Integer )
	total_amount = db.Column( db.Integer )

	created_on = db.Column( db.DateTime, default=datetime.now )
	updated_on = db.Column( db.DateTime, onupdate = datetime.now )


class TenderPickup(db.Model):

	id =  db.Column( db.Integer, primary_key=True )
	delivery_person_id = db.Column( db.Integer, db.ForeignKey('user.id') )
	tender_id = db.Column( db.Integer, db.ForeignKey('tender.id') )
	status = db.Column( db.String(200), nullable=False, default = "Assigned" )
	# Assigned/Initated/PickedUp/Delivered 
	status_updated_on = db.Column( db.DateTime, default = datetime.now )

	created_on = db.Column( db.DateTime, default=datetime.now )
	updated_on = db.Column( db.DateTime, onupdate = datetime.now )


class TenderPickupFailed(db.Model):
	
	id =  db.Column( db.Integer, primary_key=True )
	delivery_person_id = db.Column( db.Integer, db.ForeignKey('user.id') )
	tender_id = db.Column( db.Integer, db.ForeignKey('tender.id') )
	reason = db.Column( db.String(200), nullable=False)

	created_on = db.Column( db.DateTime, default=datetime.now )
	updated_on = db.Column( db.DateTime, onupdate = datetime.now )


class TenderStatusLogs(db.Model):

	id =  db.Column( db.Integer, primary_key=True )
	tender_id = db.Column( db.Integer, db.ForeignKey('tender.id') )
	status_updated_on = db.Column( db.DateTime, default = datetime.now )
	updated_by = db.Column( db.Integer, db.ForeignKey('user.id') )

	created_on = db.Column( db.DateTime, default=datetime.now  )
	updated_on = db.Column( db.DateTime, onupdate = datetime.now )

class TenderPickupStatusLogs(db.Model):

	id =  db.Column( db.Integer, primary_key=True )
	tender_pickup_id = db.Column( db.Integer, db.ForeignKey('tender_pickup.id') )
	status_updated_on = db.Column( db.DateTime, default = datetime.now )
	updated_by = db.Column( db.Integer, db.ForeignKey('user.id') )

	created_on = db.Column( db.DateTime, default=datetime.now )
	updated_on = db.Column( db.DateTime, onupdate = datetime.now )

class Transactions(db.Model):

	id =  db.Column( db.Integer, primary_key=True )
	tender_id = db.Column( db.Integer, db.ForeignKey('tender.id') )
	transaction_type = db.Column( db.String(1), nullable=False)
	amount = db.Column( db.BigInteger, nullable=False)
	mode = db.Column( db.String(200), nullable=False)
	mode_description = db.Column( db.String(200), nullable=False)
	payment_date =  db.Column( db.DateTime, nullable=False )
	description = db.Column( db.String(200), nullable=False)
	gst_percentage = db.Column( db.Integer, nullable=True )

	created_on = db.Column( db.DateTime, default=datetime.now )
	updated_on = db.Column( db.DateTime, onupdate = datetime.now )



@login_manager.user_loader
def load_user(id):
	return User.query.get(id)