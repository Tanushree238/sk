from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from admin import admin
from merchant import merchant
from delivery import delivery


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

app.register_blueprint(admin)
app.register_blueprint(merchant)
app.register_blueprint(delivery)