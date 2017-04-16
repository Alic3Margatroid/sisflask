from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
if not os.path.exists(app.instance_path):
    os.makedirs(app.instance_path)
    os.makedirs(os.path.join(app.instance_path,"ex"))
    os.makedirs(os.path.join(app.instance_path,"ch"))
from app import views, models

