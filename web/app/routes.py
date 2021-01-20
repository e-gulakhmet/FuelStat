# Данные файл содержит в себе функции для отображения страниц, по
# указанным путям


from app import flsk
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, NavigationTransForm, NavigationFuelForm, TransTableRowForm, TransTableNewRowForm, FuelTableNewRowForm, FuelTableRowForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
import sqlite3


# TODO: Убрать обновление страницы, если в этом нет нужды
# TODO: Переключение на последнюю открытую таблицу после удаления строки
# TODO: Поставить функции в определенном пораядке
# TODO: Добавить валидацию для форм в таблице


@flsk.route("/index", methods=["GET", "POST"])
@login_required # Проверяем авторизовался ли пользователь
def index():
    db = sqlite3.connect("../data/database.db")
    navig_data = list(db.execute("SELECT CAST(id as TEXT), name FROM fuel"))

    navig_trans_form = NavigationTransForm()
    navig_trans_form.names.choices = navig_data

    navig_fuel_form = NavigationFuelForm()

    trans_row_form = TransTableRowForm()

    trans_new_row_form = TransTableNewRowForm()

    fuel_row_form = FuelTableRowForm()

    fuel_new_row_form = FuelTableNewRowForm()

    # Создаем view для того, чтобы в дальнейшем не повторять условия 
    try:
        db.execute("DROP VIEW IF EXISTS vtrans")
        db.execute("""CREATE VIEW vtrans AS SELECT
                    t.id, t.fuel_id, t.dtime, t.odometer, f.name, t.amount
                    FROM trans t, fuel f WHERE t.fuel_id = f.id
                    ORDER BY t.dtime""")
    except sqlite3.Error as e:
        flsk.logger.error(e)

    try:
        db.execute("DROP VIEW IF EXISTS vfuel")
        db.execute("""CREATE VIEW vfuel AS SELECT
                      id, name, price
                      FROM fuel""")
    except sqlite3.Error as e:
        flsk.logger.error(e)

    # Проверяем, была ли нажата какая-то из submit кнопок в веб формах
    if fuel_row_form.validate_on_submit() or trans_row_form.validate_on_submit() or navig_fuel_form.validate_on_submit() or navig_trans_form.validate_on_submit() or fuel_new_row_form.validate_on_submit() or trans_new_row_form.validate_on_submit():
        flsk.logger.debug("Index page submitted")
        # Проверяем какая кнопка была нажата
        if trans_row_form.save_trans.data:
            # Если кнопка сохранения была нажата, то обновляем уже имеющуюся строку в таблице,
            # подстваляя новые значения
            flsk.logger.info("Row form save button was pressed")
            try:
                db.execute("UPDATE trans" +
                           " SET dtime = '" + str(trans_row_form.date.data) + "'" +
                           ", odometer = " + str(trans_row_form.odometer.data) +
                           ", fuel_id = " + str(trans_row_form.fuel_station.data) +
                           ", amount = " + str(trans_row_form.gallon_count.data) + 
                           " WHERE id = " + str(trans_row_form.id.data))
                db.commit()
            except sqlite3.Error as e:
                flsk.logger.error(e)
        elif navig_fuel_form.fuel_allow.data:
            # Если кнопка подтвержедения в навигационной форму была нажата,
            # то создаем новую view
            flsk.logger.debug("Navigation fuel form allow button was pressed")
            command = ("""CREATE VIEW vfuel AS SELECT
                          id, name, price
                          FROM fuel
                          WHERE price > """ + str(navig_fuel_form.start_price.data) +
                       " AND price < " + str(navig_fuel_form.end_price.data))
            navig_fuel_form.table_name.default = "fuel"
            try:
                db.execute("DROP VIEW IF EXISTS vfuel")
                db.execute(command)
            except sqlite3.Error as e:
                flsk.logger.error(e)   
        elif navig_trans_form.trans_allow.data:
            # Если кнопка подтвержедения в навигационной форме была нажата,
            # то Создаем новую view
            flsk.logger.debug("Navigation trans form allow button was pressed")
            command = ("""CREATE VIEW vtrans AS SELECT
                          t.id,  t.fuel_id, t.dtime, t.odometer, f.name, t.amount
                          FROM trans t, fuel f WHERE t.fuel_id = f.id""" +
                       " AND t.dtime > '" + str(navig_trans_form.start_date.data) + "'" +
                       " AND t.dtime < '" + str(navig_trans_form.end_date.data) + "'")
            if len(navig_trans_form.names.data) == 1:
                command += " AND t.fuel_id == " + str(navig_trans_form.names.data[0])
            elif len(navig_trans_form.names.data) != 0:
                command += " AND t.fuel_id in " + str(tuple(navig_trans_form.names.data))
            command += " ORDER BY dtime"
            try:
                db.execute("DROP VIEW IF EXISTS vtrans")
                db.execute(command)
            except sqlite3.Error as e:
                flsk.logger.error(e)
        elif trans_row_form.delete_trans.data:
            # Если была нажата кнопка удаления в веб форме строки в таблицу,
            # то удаляем строку в которой id из таблицы будет совподать с id из веб формы
            flsk.logger.debug("Row form delete button was pressed")
            try:
                db.execute("DELETE FROM trans WHERE id = " + str(trans_row_form.id.data))
                db.commit()
            except sqlite3.Error as e:
                flsk.logger.error(e)
        elif fuel_row_form.delete_fuel.data:
            # Если была нажата кнопка удаления в веб форме строки в таблицу,
            # то удаляем строку в которой id из таблицы будет совподать с id из веб формы
            flsk.logger.debug("Row form delete button was pressed")
            navig_fuel_form.table_name.default = "fuel"
            try:
                db.execute("DELETE FROM fuel WHERE id = " + str(fuel_row_form.id.data))
                db.commit()
            except sqlite3.Error as e:
                flsk.logger.error(e)
        elif trans_new_row_form.add.data:
            # Если в веб форме новой строки была нажата кнопка добавления,
            # добавляем новую строку с параментрами из веб форм
            flsk.logger.debug("New row form add button was pressed")
            try:
                db.execute("INSERT INTO trans(dtime, odometer, fuel_id, amount) VALUES (" +
                           "'" + str(trans_new_row_form.date.data) + "'" +
                           ", " + str(trans_new_row_form.odometer.data) + 
                           ", " + str(trans_new_row_form.fuel_station.data) +
                           ", " + str(trans_new_row_form.gallon_count.data) + ")")
            except sqlite3.Error as e:
                flsk.logger.error(e)
            db.commit()
        else:
            return
    # Достаем данные о заправлках из базы данных
    try:
        trans_data = db.execute("""SELECT id, fuel_id, dtime, odometer, name, amount
                                FROM vtrans""")
    except sqlite3.Error as e:
        flsk.logger.error(e)
    try:
        fuel_data = db.execute("""SELECT id, name, price
                                FROM vfuel""")
    except sqlite3.Error as e:
        flsk.logger.error(e)

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
                           fuel_new_row_form=fuel_new_row_form)



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
    # Генерируем страницу авторизиции
    flsk.logger.debug("Rendering login page")
    return render_template("login.html", title="Login", form=form)



@flsk.route('/logout')
@login_required
def logout():
    flsk.logger.info("User logouted")
    logout_user()
    return redirect(url_for('index'))