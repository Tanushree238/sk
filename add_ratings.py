from app.models import *
import random

for product in Product.query.all():
    if product.rating is None:
        product.rating = round(random.random(),1) + random.randrange(3,4)
        db.session.commit()