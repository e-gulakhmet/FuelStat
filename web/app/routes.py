# Данные файл содержит в себе функции для отображения страниц, по
# указанным путям

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import flsk
from app.forms import LoginForm, NavigationTransForm, NavigationFuelForm
from app.forms import TransTableRowForm, TransTableNewRowForm
from app.forms import FuelTableNewRowForm, FuelTableRowForm
from app.models import User
from app.database import DataBase


# TODO: Убрать обновление страницы, если в этом нет нужды
# TODO: Добавить валидацию для форм в таблице
# TODO: Сделать разные логгеры для каждого из классов или файлов
# TODO: Заменить str condition в database.py на tuple condition


@flsk.route("/index", methods=["GET", "POST"])
@login_required # Проверяем авторизовался ли пользователь
def index():
    db = DataBase("../data/database.db")
    navig_data = list(db.select("name", "CAST(id as TEXT), name"))

    navig_trans_form = NavigationTransForm()
    navig_trans_form.names.choices = navig_data

    navig_fuel_form = NavigationFuelForm()

    trans_row_form = TransTableRowForm()

    trans_new_row_form = TransTableNewRowForm()

    fuel_row_form = FuelTableRowForm()

    fuel_new_row_form = FuelTableNewRowForm()

    table_name = "trans"

    # Создаем view для того, чтобы в дальнейшем не повторять условия 
    db.create_view("vtrans", "trans t, fuel f",
                   "t.id, t.fuel_id, t.dtime, t.odometer, f.name, t.amount",
                   "t.fuel_id = f.id", "t.dtime", re_create=True)
    db.create_view("vfuel", "fuel", "id, name, price", re_create=True)

    # Проверяем, была ли нажата какая-то из submit кнопок в веб формах
    if (fuel_row_form.validate_on_submit() 
       or trans_row_form.validate_on_submit()
       or navig_fuel_form.validate_on_submit()
       or navig_trans_form.validate_on_submit()
       or fuel_new_row_form.validate_on_submit()
       or trans_new_row_form.validate_on_submit()):
        flsk.logger.debug("Index submit button was pressed")
        # Проверяем какая кнопка была нажата
        if trans_row_form.save_trans.data:
            # Если кнопка сохранения была нажата, то обновляем уже имеющуюся строку в таблице,
            # подстваляя новые значения
            flsk.logger.debug("Save button was pressed in the row of the trans table")
            db.update("trans", 
                      ("dtime = '" + str(trans_row_form.date.data) + "'" +
                       ", odometer = " + str(trans_row_form.odometer.data) +
                       ", fuel_id = " + str(trans_row_form.fuel_station.data) +
                       ", amount = " + str(trans_row_form.gallon_count.data)),
                      "id = " + str(trans_row_form.id.data))
            db.commit()
            table_name = "trans"
        elif fuel_row_form.save_fuel.data:
            # Если кнопка сохранения была нажата, то обновляем уже имеющуюся строку в таблице,
            # подстваляя новые значения
            flsk.logger.debug("Save button was pressed in the row of the fuel table")
            db.update("fuel",
                      "name = '" + str(fuel_row_form.name.data) + "'" +
                      ", price = " + str(fuel_row_form.price.data),
                      "id = " + str(fuel_row_form.id.data))
            db.commit()
            table_name = "fuel"

        elif navig_trans_form.trans_allow.data:
            # Если кнопка подтвержедения в навигационной форме была нажата,
            # то Создаем новую view
            flsk.logger.debug("Allow button was pressed in the trans navigation")
            condition = ("t.fuel_id = f.id" +
                         " AND t.dtime > '" + str(navig_trans_form.start_date.data) + "'" +
                         " AND t.dtime < '" + str(navig_trans_form.end_date.data) + "'")
            if len(navig_trans_form.names.data) == 1:
                condition += " AND t.fuel_id == " + str(navig_trans_form.names.data[0])
            elif len(navig_trans_form.names.data) != 0:
                condition += " AND t.fuel_id in " + str(tuple(navig_trans_form.names.data))
            db.create_view("vtrans", "trans t, fuel f",
                           "t.id,  t.fuel_id, t.dtime, t.odometer, f.name, t.amount",
                           condition, "dtime", re_create=True)
            db.commit()
            table_name = "trans"
        elif navig_fuel_form.fuel_allow.data:
            # Если кнопка подтвержедения в навигационной форму была нажата,
            # то создаем новую view
            flsk.logger.debug("Allow button was pressed in the fuel navigation")
            db.create_view("vfuel", "fuel", "id, name, price",
                           ("price > " + str(navig_fuel_form.start_price.data) +
                            " AND price < " + str(navig_fuel_form.end_price.data)),
                           re_create=True)
            db.commit()
            table_name = "fuel"

        elif trans_row_form.delete_trans.data:
            # Если была нажата кнопка удаления в веб форме строки в таблицу,
            # то удаляем строку в которой id из таблицы будет совподать с id из веб формы
            flsk.logger.debug("Delete button was pressed in the row of the trans table")
            db.delete("trans", "id = " + str(trans_row_form.id.data))
            db.commit()
            table_name = "trans"
        elif fuel_row_form.delete_fuel.data:
            # Если была нажата кнопка удаления в веб форме строки в таблицу,
            # то удаляем строку в которой id из таблицы будет совподать с id из веб формы
            flsk.logger.debug("Delete button was pressed in the row of the fuel table")
            db.delete("fuel", "id = " + str(fuel_row_form.id.data))
            db.commit()
            table_name = "fuel"

        elif trans_new_row_form.add_trans.data:
            # Если в веб форме новой строки, была нажата кнопка добавления,
            # добавляем новую строку с параментрами из веб форм
            flsk.logger.debug("Add button was pressed in the new row of the trans table")
            db.insert("trans", "dtime, odometer, fuel_id, amount",
                      ("'" + str(trans_new_row_form.date.data) + "'" +
                       ", " + str(trans_new_row_form.odometer.data) + 
                       ", " + str(trans_new_row_form.fuel_station.data) +
                       ", " + str(trans_new_row_form.gallon_count.data)))
            table_name = "trans"
        elif fuel_new_row_form.add_fuel.data:
            # Если в веб форме новой строки, была нажата кнопка добавления,
            # добавляем новую строку с параментрами из веб форм
            flsk.logger.debug("Add button was pressed in the new row of the fuel table")
            db.insert("fuel", "name, price", 
                      ("'" + str(fuel_new_row_form.name.data) + "'" +
                       ", " + str(fuel_new_row_form.price.data)))
            table_name = "fuel"
    # Достаем данные о заправлках из базы данных
    flsk.logger.debug("Selecting data from trans view")
    trans_data = db.select("vtrans",
                           "id, fuel_id, dtime, odometer, name, amount")
    flsk.logger.debug("Selecting data from fuel view")
    fuel_data = db.select("vfuel", "id, name, price")

    # Обновляем страницу
    flsk.logger.debug("Rendering index page")
    return render_template("index.html",
                           trans_data=trans_data,
                           fuel_data=fuel_data,
                           navig_trans_form=navig_trans_form,
                           navig_fuel_form=navig_fuel_form,
                           trans_row_form=trans_row_form,
                           trans_new_row_form=trans_new_row_form,
                           fuel_row_form=fuel_row_form,
                           fuel_new_row_form=fuel_new_row_form,
                           table_name=table_name)



@flsk.route("/", methods=["GET", "POST"])
@flsk.route("/login", methods=["GET", "POST"])
def login():
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
        flsk.logger.info("User already autheticated")
        return redirect(url_for('index'))
    # Создаем объект form, который содержит в себе веб-формы для
    # авторизации
    form = LoginForm()
    # Если пришел POST запрос от браузера
    if form.validate_on_submit():
        flsk.logger.debug("L0gin page submitted")
        if user.username != form.username.data or user.check_password(form.password.data) is False:
            flsk.logger.info("Invalid username or password")
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # Иначе загружаем пользователя
        # и переходим к основной странице
        login_user(user, remember=form.remember.data)
        flsk.logger.info("User" + user.username + " signed in")
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
    flsk.logger.debug("Rendering login page")
    return render_template("login.html", title="Login", form=form)



@flsk.route('/logout')
@login_required
def logout():
    flsk.logger.info("User logouted")
    logout_user()
    return redirect(url_for('index'))
