import numpy as np
import pandas as pd
import psycopg2
import sklearn
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
conn = psycopg2.connect(database="sk_final", user = "tanu", password = "1234", host = "127.0.0.1", port = "5432")

if conn:
	print("Opened database successfully")
cur = conn.cursor()

def fetch_popular_product_categories():
	cur.execute("SELECT id, name, specifications, category_id, rating  from product where rating is not NULL")
	rows = cur.fetchall()
	rowarray_list = {'id':[], 'name':[], 'specifications':[],'category': [],'ratings':[]}
	for row in rows:
		rowarray_list["id"].append(row[0])
		rowarray_list["name"].append(row[1])
		rowarray_list["specifications"].append(row[2])
		rowarray_list["category"].append(row[3])
		rowarray_list["ratings"].append(row[4])
	data = rowarray_list
	product_ratings = pd.DataFrame(data)
	popular_products = pd.DataFrame(product_ratings.groupby('category')['ratings'].mean())
	most_popular = popular_products.sort_values('ratings', ascending=False)
	return most_popular

def fetch_recommended_cluster(search_text):
	cur.execute("SELECT id, name, specifications  from product")
	rows = cur.fetchall()
	rowarray_list = {'id':[], 'name':[], 'specifications':[]}
	for row in rows:
		rowarray_list["id"] .append(row[0])
		rowarray_list["name"] .append(row[1])
		rowarray_list["specifications"] .append(row[1])

	data = rowarray_list
	product_descriptions = pd.DataFrame(data)
	product_descriptions.shape
	product_descriptions1 = product_descriptions
	vectorizer = TfidfVectorizer(stop_words='english')
	X1 = vectorizer.fit_transform(product_descriptions1["name"])
	kmeans = KMeans(n_clusters = 10, init = 'k-means++')
	y_kmeans = kmeans.fit_predict(X1)
	true_k = 10
	model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
	model.fit(X1)

	order_centroids = model.cluster_centers_.argsort()[:, ::-1]
	terms = vectorizer.get_feature_names()
	Y = vectorizer.transform([search_text])
	prediction = model.predict(Y)
	cluster = []
	for ind in order_centroids[prediction[0], :10]:
		cluster.append(' %s' % terms[ind])
	return cluster
	
