from flask import Flask
from flask_login import LoginManager
from config import Config
import logging
import os

flsk = Flask(__name__)
flsk.config.from_object(Config)

login = LoginManager(flsk)
# Страница, которую получит пользователь, если не авторизуется,
# но захочет зайти на страницу для зарегистированных пользователей
login.login_view = 'login'
login.login_message = "Please Sign In"

logging.basicConfig(filename=os.path.join(flsk.config["PROJECT_FOLDER"], 'logging.log'),
                    level=logging.DEBUG,
                    format="%(asctime)s %(name)s [%(levelname)s] : %(message)s, line %(lineno)d in %(filename)s'))")

from app.index import bp as index_bp
flsk.register_blueprint(index_bp)

from app.login import bp as login_bp
flsk.register_blueprint(login_bp)

from app.upload import bp as upload_bp
flsk.register_blueprint(upload_bp)