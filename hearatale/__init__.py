from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

login_manager = LoginManager()

db = SQLAlchemy(app)
login_manager.init_app(app)


@app.route("/")
def home():
    return "Hello, World!"

from models import *