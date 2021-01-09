from flask import Flask
from flask_login import LoginManager
import logging

flsk = Flask(__name__)
flsk.config["SECRET_KEY"] = "pedaling"

login = LoginManager(flsk)
# Страница, которую получит пользователь, если не авторизуется,
# но захочет зайти на страницу для зарегистированных пользователей
login.login_view = 'login'
login.login_message = "Please Sign In"

logging.basicConfig(filename='logging.log',
                    level=logging.DEBUG,
                    format="%(asctime)s %(name)s [%(levelname)s] : %(message)s")

from app import routes