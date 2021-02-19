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

from app import routes