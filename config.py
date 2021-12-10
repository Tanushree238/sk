import os
from datetime import date

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or "!@#%^&*(*&^%@$#%^&*()*&^%hjbcjhdfcgvhjnkcwebkjnwejweegSFDGHCJDW!@#$%^&*(*&^%$"

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or "postgresql://tanu:1234@localhost:5432/sk_final"
  
    SQLALCHEMY_TRACK_MODIFICATIONS = False
