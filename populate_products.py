import csv
import os
import os
from app.models import *

csv_list = []
dir_list = []
directory = 'app/static/products_data/'
for filename in os.listdir(directory):
	sub_path = directory+filename
	if os.path.isdir(sub_path):
		dir_list.append(sub_path+"/"+os.listdir(sub_path)[0]+"/")
	if filename.endswith(".csv"):
		csv_list.append(filename)
csv_list.sort()
dir_list.sort()

count = 0
products_data = {}
count = len(csv_list)
for i in range(count):
	images = set()
	for image in  os.listdir(dir_list[i]):
		images.add(image)
	prod_list = []
	with open(directory+csv_list[i], mode='r') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			for image in images:
				image_name = ".".join((image.split(".")[:-1]))
				image_name = " ".join(image_name.split("-"))
				if row["Name"].strip(".").strip(" ") in image_name:
					spec = row["Specifications"] if "Specifications" in row else None
					rating = row["Ratings"] if "Ratings" in row else None
					prod = {
						"name" : image_name,
						"price" : row["Price"].strip("₹"),
						"specifications" : spec,
						"rating" : rating,
						"image" : dir_list[i]+ image
					}
					prod_list.append(prod)
	products_data[csv_list[i]]=prod_list
	count += len(prod_list)
	print(csv_list[i], count)
for category, products in products_data.items():
	category_name = category.split(".csv")[0]
	category_obj = ProductCategory.query.filter_by(name=category_name).first()
	if not category_obj:
		category_obj = ProductCategory(name=category_name)
		db.session.add(category_obj)
		db.session.commit()
	print("{} category obj created".format(category_name))
	for product in products:
		product_obj = Product.query.filter_by(name=product["name"]).first()
		if not product_obj:
			with open("app/static/product_images/"+product["name"]+".jpg", "wb") as out_file:
				with open(product["image"], "rb") as in_file:
					out_file.write(in_file.read())
			price = int("".join(product["price"].split(",")))
			product_obj = Product(
				name = product["name"],
				marked_retail_price = price,
				stock_quantity = 0,
				specifications = product['specifications'],
				rating = product['rating'],
				image = product["name"]+".jpg",
				category_id = category_obj.id
			)
			db.session.add(product_obj)
			db.session.commit()
			print("{} product obj created".format(product["name"]))	  