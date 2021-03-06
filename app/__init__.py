from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)

login_manager.login_view = "login"
login_manager.blueprint_login_views = {
    "admin": "admin.login",
    "merchant": "merchant.login",
    "delivery": "delivery.login",
    "user": "login"
}

login_manager.login_message_category = 'info'

from app import routes, models
from admin import admin
from merchant import merchant
from delivery import delivery
from user import user

app.register_blueprint(admin)
app.register_blueprint(merchant)
app.register_blueprint(user)
app.register_blueprint(delivery)
