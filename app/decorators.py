from flask import request, redirect, url_for, flash
from flask_login import current_user


def check_role(role):
	
	def check_decorator(function):
		def check(*args,**kwargs):
			if current_user.is_authenticated:
				if role in current_user.get_roles():
					return function(*args,**kwargs)
				else:
					if role =="Merchant":
						flash('Permission Denied', "danger")
						if "Admin" in current_user.get_roles():
							return redirect(url_for("admin.login"))
						elif "Delivery" in current_user.get_roles():
							return redirect(url_for("delivery.login"))
						elif "User" in current_user.get_roles():
							return redirect(url_for(".login"))
					else:
						flash('Permission Denied', "danger")
						return redirect(url_for(".dashboard"))
			return redirect(url_for(".login"))

		return check

	return check_decorator

		