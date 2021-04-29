from app import app,db 
from sqlalchemy.orm import backref
from datetime import datetime
from time import time
from flask import url_for
from time import time
import os
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func,text


class User(db.Model):

	id = db.Column( db.Integer, primary_key=True )
	name = db.Column( db.String(100), nullable=False )
	contact = db.Column( db.BigInteger, unique=True, nullable=False)
	email = db.Column( db.String(40), nullable=False, unique=True )
	password = db.Column( db.String(255), nullable=False )

	user_roles = db.relationship('UserRole', backref="user", lazy="dynamic", cascade="save-update, delete")

	created_on = db.Column( db.DateTime, default=datetime.now )
	updated_on = db.Column( db.DateTime, onupdate = datetime.now )
 
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
	description = db.Column( db.Text )

	category_id = db.Column( db.Integer, db.ForeignKey('product_category.id') )
	product_images = db.relationship('ProductImage', backref="product", lazy="dynamic", cascade="save-update, delete")

	created_on = db.Column( db.DateTime, default=datetime.now )
	updated_on = db.Column( db.DateTime, onupdate = datetime.now )
 
	def __repr__(self):
		return self.name


class ProductImage(db.Model):

	id = db.Column( db.Integer, primary_key=True )
	product_id = db.Column( db.Integer, db.ForeignKey('product.id') )
	image = db.Column( db.String(200), nullable=False )

	created_on = db.Column( db.DateTime, default=datetime.now )
	updated_on = db.Column( db.DateTime, onupdate = datetime.now )
 
	def __repr__(self):
		return self.image


class Tender(db.Model):


	id = db.Column( db.Integer, primary_key=True )
	user_id = db.Column( db.Integer, db.ForeignKey('user.id') )
    Products (rel) 
    total_amount = db.Column(db.Integer)
    advance_amount = db.Column(db.Integer)
    paid_amount = db.Column(db.Integer)
    pickup_date = db.Column( db.DateTime ) 
	status = db.Column( db.String(200), nullable=False, default = Draft)
	status_updated_on = db.Column( db.DateTime)

	created_on = db.Column( db.DateTime, default=datetime.now )
	updated_on = db.Column( db.DateTime, onupdate = datetime.now )
  
TenderProductMapper
    Pid
    Quantity 
    Price of 1 Prod
    TotalAmount
    Adv percentage 

TenderPickup 
    Uid 
    Tid
    Status 

TenderPickupFailed
    Uid
    Tid
    Reason

TenderStatusLogs
    Tid
    Status
    StatusUpdatedOn
    UpdatedBy (Admin - Uid)
 
Transactions
    MId
    Tid
    TransType 
    Amount
    Mode
    Mode Desc
    Payment Date
    Desc
    GST P
