from flask import Flask

flsk = Flask(__name__)
flsk.config["SECRET_KEY"] = "pedaling"

from app import routes