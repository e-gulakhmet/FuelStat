from flask import Blueprint

bp = Blueprint('upload', __name__, template_folder="templates")

from app.upload import routes