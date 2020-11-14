from flask import Flask
from flask_login import LoginManager

flsk = Flask(__name__)
flsk.config["SECRET_KEY"] = "pedaling"

login = LoginManager(flsk)

from app import routes