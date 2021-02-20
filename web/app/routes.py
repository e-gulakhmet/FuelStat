# Данные файл содержит в себе функции для отображения страниц, по
# указанным путям

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import logging
import os

from app import flsk
from app.forms import LoginForm
from app.forms import UploadFuelForm, UploadTransForm
from app.models import User
from app.funcs import update_file, replace_file



@flsk.route("/upload", methods=["GET", "POST"])
@login_required # Проверяем авторизовался ли пользователь
def upload():
    logger = logging.getLogger("UPLOAD")
    upload_trans_form = UploadTransForm()
    upload_fuel_form = UploadFuelForm()

    if upload_fuel_form.validate_on_submit() and upload_fuel_form.upload_fuel.data:
        logger.debug("Upload fuel form button was pressed")
        # Если был выбран метод добавление данных файлв к уже имеющимся
        path_to_old_file = flsk.config["PROJECT_FOLDER"] + "/../data/fuel.csv"
        if upload_fuel_form.method_fuel.data == "0":
            update_file(upload_fuel_form.file_fuel.data, path_to_old_file,
                        "fuel", logger)
        # Если был выбран режим замены старого файла новым
        elif upload_fuel_form.method_fuel.data == "1":
            replace_file(upload_fuel_form.file_fuel.data,
                         path_to_old_file, "fuel", logger)
    
    if upload_trans_form.validate_on_submit() and upload_trans_form.upload_trans.data:
        logger.debug("Upload trans form button was pressed")
        # Если был выбран метод добавление данных файлв к уже имеющимся
        path_to_old_file = flsk.config["PROJECT_FOLDER"] + "/../data/trans.csv"
        if upload_trans_form.method_trans.data == "0":
            update_file(upload_trans_form.file_trans.data,
                        path_to_old_file,
                        "trans", logger)
        # Если был выбран режим замены старого файла новым
        elif upload_trans_form.method_trans.data == "1":
            replace_file(upload_trans_form.file_trans.data,
                         path_to_old_file,
                         "trans", logger)
        
        # Говорим программе, которая создает репорт, обновить базу данных
        os.system("python " +
                  os.path.join(flsk.config["FUELSTAT_FOLDER"], "main.py") +
                  " --load --recreate")

    return render_template("upload.html",
                           upload_trans_form=upload_trans_form,
                           upload_fuel_form=upload_fuel_form)


@flsk.route("/", methods=["GET", "POST"])
@flsk.route("/login", methods=["GET", "POST"])
def login():
    logger = logging.getLogger("LOGIN")

    # При входе на сайт, пользователь сразу переходит к странице
    # авторизации.
    # Он вводит свой логин и пароль, а так как пользователь у нас один,
    # то проверяем введенные данные с данными, которые у нас есть.
    # Если были введены верные данные, то переводим его на основную
    # страницу.
    # Иначе просим его ввести данные снова.

    user = User("admin", "admin")

    # Проверяем, если пользователь уже зашел,
    # то отправляем его на основную страницу.
    if current_user.is_authenticated:
        logger.info("User already autheticated")
        return redirect(url_for("index.index"))
    # Создаем объект form, который содержит в себе веб-формы для
    # авторизации
    form = LoginForm()
    # Если пришел POST запрос от браузера
    if form.validate_on_submit():
        logger.debug("L0gin page submitted")
        if user.username != form.username.data or user.check_password(form.password.data) is False:
            logger.info("Invalid username or password")
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # Иначе загружаем пользователя
        # и переходим к основной странице
        login_user(user, remember=form.remember.data)
        logger.info("User" + user.username + " signed in")
        # Проверяем, если в строке был указан аргумент next,
        # значит пользователь пытался перейти на страницу для
        # авторизованных пользователей, но так как он не авторизовалься,
        # его перенаправили сюда. Тогда после того, как он
        # авторизовался, переходим на стрницу указанную страницу.
        next_page = request.args.get("next")
        # Если аргумента next нет, то переходим на главную страницу
        if next_page is None or url_parse(next_page).netloc != '':
            next_page = url_for("index")
        return redirect(next_page)
    # Отображаем страницу авторизиции
    logger.debug("Rendering login page")
    return render_template("login.html", title="Login", form=form)



@flsk.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
