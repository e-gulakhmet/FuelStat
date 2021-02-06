# Данные файл содержит в себе функции для отображения страниц, по
# указанным путям

from flask import render_template, flash, redirect, url_for, request, send_file
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import logging
import os

from app import flsk
from app.forms import LoginForm, NavigationTransForm, NavigationFuelForm
from app.forms import TransTableRowForm, TransTableNewRowForm
from app.forms import FuelTableNewRowForm, FuelTableRowForm, ReportForm
from app.models import User
from app.database import DataBase


# TODO: Убрать обновление страницы, если в этом нет нужды
# TODO: Проверка введенных данных в js
# TODO: Подсвечивание данных, которые введены не верно


@flsk.route("/index", methods=["GET", "POST"])
@login_required # Проверяем авторизовался ли пользователь
def index():

    logger = logging.getLogger("INDEX")
    
    db = DataBase(__file__.replace("web/app/routes.py", "data/database.db"))
    stations_info = list(db.select("fuel", "CAST(id as TEXT), name"))

    navig_trans_form = NavigationTransForm()
    navig_trans_form.names.choices = stations_info

    navig_fuel_form = NavigationFuelForm()

    trans_row_form = TransTableRowForm()

    trans_new_row_form = TransTableNewRowForm()

    fuel_row_form = FuelTableRowForm()

    fuel_new_row_form = FuelTableNewRowForm()

    report_form = ReportForm()
    report_form.names.choices = stations_info

    table_name = "trans"

    # Создаем view для того, чтобы в дальнейшем не повторять условия 
    db.create_view("vtrans", "trans t, fuel f",
                   "t.id, t.fuel_id, t.dtime, t.odometer, f.name, t.amount",
                   "t.fuel_id = f.id", "t.dtime", re_create=True)
    db.create_view("vfuel", "fuel", "id, name, price", re_create=True)

    if request.method == "POST":
        print(navig_trans_form.validate_on_submit())
        print(navig_fuel_form.validate_on_submit())
        print(trans_row_form.validate())
        print(fuel_row_form.validate_on_submit())
        print(trans_new_row_form.validate_on_submit())
        print(fuel_new_row_form.validate_on_submit())
        print("\n")

    if request.method == "POST":
        # Проверяем, была ли нажата какая-то из submit кнопок в веб формах
        if navig_trans_form.validate() and navig_trans_form.trans_allow.data:
            # Если кнопка подтвержедения в навигационной форме была нажата,
            # то Создаем новую view
            logger.debug("Allow button was pressed in the trans navigation")
            condition = ("t.fuel_id = f.id" +
                         " AND t.dtime > '" + str(navig_trans_form.start_date.data) + "'" +
                         " AND t.dtime < '" + str(navig_trans_form.end_date.data) + "'" +
                         " AND t.odometer > " + str(navig_trans_form.start_odometer.data) +
                         " AND t.odometer < " + str(navig_trans_form.end_odometer.data))
            if len(navig_trans_form.names.data) == 1:
                condition += " AND t.fuel_id == " + str(navig_trans_form.names.data[0])
            elif len(navig_trans_form.names.data) != 0:
                condition += " AND t.fuel_id in " + str(tuple(navig_trans_form.names.data))
            db.create_view("vtrans", "trans t, fuel f",
                           "t.id,  t.fuel_id, t.dtime, t.odometer, f.name, t.amount",
                           condition, "dtime", re_create=True)
            db.commit()
            table_name = "trans"

        elif navig_fuel_form.validate() and navig_fuel_form.fuel_allow.data:
            # Если кнопка подтвержедения в навигационной форму была нажата,
            # то создаем новую view
            logger.debug("Allow button was pressed in the fuel navigation")
            db.create_view("vfuel", "fuel", "id, name, price",
                           ("price > " + str(navig_fuel_form.start_price.data) +
                            " AND price < " + str(navig_fuel_form.end_price.data)),
                           re_create=True)
            db.commit()
            table_name = "fuel"

        elif trans_row_form.validate() and (trans_row_form.save_trans.data or trans_row_form.delete_trans.data):
            if trans_row_form.save_trans.data:
                # Если кнопка сохранения была нажата, то обновляем уже имеющуюся строку в таблице,
                # подстваляя новые значения
                logger.debug("Save button was pressed in the row of the trans table")
                db.update("trans", 
                          ("dtime = '" + str(trans_row_form.date.data) + "'" +
                           ", odometer = " + str(trans_row_form.odometer.data) +
                           ", fuel_id = " + str(trans_row_form.fuel_station.data) +
                           ", amount = " + str(trans_row_form.gallon_count.data)),
                          "id = " + str(trans_row_form.id.data))
                db.commit()
                table_name = "trans"
            elif trans_row_form.delete_trans.data:
                # Если была нажата кнопка удаления в веб форме строки в таблицу,
                # то удаляем строку в которой id из таблицы будет совподать с id из веб формы
                logger.debug("Delete button was pressed in the row of the trans table")
                db.delete("trans", "id = " + str(trans_row_form.id.data))
                db.commit()
                table_name = "trans"
        
        elif fuel_row_form.validate() and (fuel_row_form.save_fuel.data or fuel_row_form.delete_fuel.data):
            if fuel_row_form.save_fuel.data:
                # Если кнопка сохранения была нажата, то обновляем уже имеющуюся строку в таблице,
                # подстваляя новые значения
                logger.debug("Save button was pressed in the row of the fuel table")
                db.update("fuel",
                          ("name = '" + str(fuel_row_form.name.data) + "'" +
                           ", price = " + str(fuel_row_form.price.data)),
                          "id = " + str(fuel_row_form.id.data))
                db.commit()
                table_name = "fuel"
            elif fuel_row_form.delete_fuel.data:
                # Если была нажата кнопка удаления в веб форме строки в таблицу,
                # то удаляем строку в которой id из таблицы будет совподать с id из веб формы
                logger.debug("Delete button was pressed in the row of the fuel table")
                db.delete("fuel", "id = " + str(fuel_row_form.id.data))
                db.commit()
                table_name = "fuel"
        
        elif trans_new_row_form.validate() and trans_new_row_form.add_trans.data:
            # Если в веб форме новой строки, была нажата кнопка добавления,
            # добавляем новую строку с параментрами из веб форм
            logger.debug("Add button was pressed in the new row of the trans table")
            db.insert("trans", "dtime, odometer, fuel_id, amount",
                      ("'" + str(trans_new_row_form.date.data) + "'" +
                       ", " + str(trans_new_row_form.odometer.data) + 
                       ", " + str(trans_new_row_form.fuel_station.data) +
                       ", " + str(trans_new_row_form.gallon_count.data)))
            table_name = "trans"
        
        elif fuel_new_row_form.validate() and fuel_new_row_form.add_fuel.data:
            # Если в веб форме новой строки, была нажата кнопка добавления,
            # добавляем новую строку с параментрами из веб форм
            logger.debug("Add button was pressed in the new row of the fuel table")
            db.insert("fuel", "name, price", 
                      ("'" + str(fuel_new_row_form.name.data) + "'" +
                       ", " + str(fuel_new_row_form.price.data)))
            table_name = "fuel"
        
        elif report_form.validate() and report_form.get_report.data:
            # Если кнопка подтвержедения в навигационной форме была нажата,
            # то Создаем новую view
            logger.debug("Allow button was pressed in the report")
            report_param = (" --report" +
                            " --startdate " + str(report_form.start_date.data) +
                            " --enddate " + str(report_form.end_date.data) +
                            " --startodometer " + str(report_form.start_odometer.data) +
                            " --endodometer " + str(report_form.end_odometer.data))
            if report_form.names.data is not None:
                for i in report_form.names.data:
                    for station in stations_info:
                        if station[0] == i:
                            report_param += " --gasname " + station[1]
                            break
            if report_form.show_statistic.data:
                report_param += " --statistic"
            if report_form.show_table.data:
                report_param += " --info"
            os.system("python " +
                      __file__.replace("web/app/routes.py", "main.py") +
                      report_param)
            return send_file(__file__.replace("web/app/routes.py", "data/report.pdf"), attachment_filename="report.pdf")
        


    # if (fuel_row_form.validate_on_submit() 
    #    or trans_row_form.validate_on_submit()
    #    or navig_fuel_form.validate_on_submit()
    #    or navig_trans_form.validate_on_submit()
    #    or fuel_new_row_form.validate_on_submit()
    #    or trans_new_row_form.validate_on_submit()):
    #     logger.debug("Index submit button was pressed")
    #     print(fuel_row_form.validate_on_submit())
    #     print(trans_row_form.validate_on_submit())
    #     print(navig_fuel_form.validate_on_submit())
    #     print(navig_trans_form.validate_on_submit())
    #     print(fuel_new_row_form.validate_on_submit())
    #     print(trans_new_row_form.validate_on_submit())
    #     # Проверяем какая кнопка была нажата
    #     if trans_row_form.save_trans.data:
    #         # Если кнопка сохранения была нажата, то обновляем уже имеющуюся строку в таблице,
    #         # подстваляя новые значения
    #         logger.debug("Save button was pressed in the row of the trans table")
    #         db.update("trans", 
    #                   ("dtime = '" + str(trans_row_form.date.data) + "'" +
    #                    ", odometer = " + str(trans_row_form.odometer.data) +
    #                    ", fuel_id = " + str(trans_row_form.fuel_station.data) +
    #                    ", amount = " + str(trans_row_form.gallon_count.data)),
    #                   "id = " + str(trans_row_form.id.data))
    #         db.commit()
    #         table_name = "trans"
    #     elif fuel_row_form.save_fuel.data:
    #         # Если кнопка сохранения была нажата, то обновляем уже имеющуюся строку в таблице,
    #         # подстваляя новые значения
    #         logger.debug("Save button was pressed in the row of the fuel table")
    #         db.update("fuel",
    #                   "name = '" + str(fuel_row_form.name.data) + "'" +
    #                   ", price = " + str(fuel_row_form.price.data),
    #                   "id = " + str(fuel_row_form.id.data))
    #         db.commit()
    #         table_name = "fuel"

    #     elif navig_trans_form.trans_allow.data:
    #         # Если кнопка подтвержедения в навигационной форме была нажата,
    #         # то Создаем новую view
    #         logger.debug("Allow button was pressed in the trans navigation")
    #         condition = ("t.fuel_id = f.id" +
    #                      " AND t.dtime > '" + str(navig_trans_form.start_date.data) + "'" +
    #                      " AND t.dtime < '" + str(navig_trans_form.end_date.data) + "'" +
    #                      " AND t.odometer > " + str(navig_trans_form.start_odometer.data) +
    #                      " AND t.odometer < " + str(navig_trans_form.end_odometer.data))
    #         if len(navig_trans_form.names.data) == 1:
    #             condition += " AND t.fuel_id == " + str(navig_trans_form.names.data[0])
    #         elif len(navig_trans_form.names.data) != 0:
    #             condition += " AND t.fuel_id in " + str(tuple(navig_trans_form.names.data))
    #         db.create_view("vtrans", "trans t, fuel f",
    #                        "t.id,  t.fuel_id, t.dtime, t.odometer, f.name, t.amount",
    #                        condition, "dtime", re_create=True)
    #         db.commit()
    #         table_name = "trans"
    #     elif navig_fuel_form.fuel_allow.data:
    #         # Если кнопка подтвержедения в навигационной форму была нажата,
    #         # то создаем новую view
    #         logger.debug("Allow button was pressed in the fuel navigation")
    #         db.create_view("vfuel", "fuel", "id, name, price",
    #                        ("price > " + str(navig_fuel_form.start_price.data) +
    #                         " AND price < " + str(navig_fuel_form.end_price.data)),
    #                        re_create=True)
    #         db.commit()
    #         table_name = "fuel"

    #     elif trans_row_form.delete_trans.data:
    #         # Если была нажата кнопка удаления в веб форме строки в таблицу,
    #         # то удаляем строку в которой id из таблицы будет совподать с id из веб формы
    #         logger.debug("Delete button was pressed in the row of the trans table")
    #         db.delete("trans", "id = " + str(trans_row_form.id.data))
    #         db.commit()
    #         table_name = "trans"
    #     elif fuel_row_form.delete_fuel.data:
    #         # Если была нажата кнопка удаления в веб форме строки в таблицу,
    #         # то удаляем строку в которой id из таблицы будет совподать с id из веб формы
    #         logger.debug("Delete button was pressed in the row of the fuel table")
    #         db.delete("fuel", "id = " + str(fuel_row_form.id.data))
    #         db.commit()
    #         table_name = "fuel"

    #     elif trans_new_row_form.add_trans.data:
    #         # Если в веб форме новой строки, была нажата кнопка добавления,
    #         # добавляем новую строку с параментрами из веб форм
    #         logger.debug("Add button was pressed in the new row of the trans table")
    #         db.insert("trans", "dtime, odometer, fuel_id, amount",
    #                   ("'" + str(trans_new_row_form.date.data) + "'" +
    #                    ", " + str(trans_new_row_form.odometer.data) + 
    #                    ", " + str(trans_new_row_form.fuel_station.data) +
    #                    ", " + str(trans_new_row_form.gallon_count.data)))
    #         table_name = "trans"
    #     elif fuel_new_row_form.add_fuel.data:
    #         # Если в веб форме новой строки, была нажата кнопка добавления,
    #         # добавляем новую строку с параментрами из веб форм
    #         logger.debug("Add button was pressed in the new row of the fuel table")
    #         db.insert("fuel", "name, price", 
    #                   ("'" + str(fuel_new_row_form.name.data) + "'" +
    #                    ", " + str(fuel_new_row_form.price.data)))
    #         table_name = "fuel"

    #     elif report_form.get_report.data:
    #         # Если кнопка подтвержедения в навигационной форме была нажата,
    #         # то Создаем новую view
    #         logger.debug("Allow button was pressed in the report")
    #         report_param = (" --report" +
    #                         " --startdate " + str(report_form.start_date.data) +
    #                         " --enddate " + str(report_form.end_date.data) +
    #                         " --startodometer " + str(report_form.start_odometer.data) +
    #                         " --endodometer " + str(report_form.end_odometer.data))
    #         if report_form.names.data is not None:
    #             for i in report_form.names.data:
    #                 for station in stations_info:
    #                     if station[0] == i:
    #                         report_param += " --gasname " + station[1]
    #                         break
    #         if report_form.show_statistic.data:
    #             report_param += " --statistic"
    #         if report_form.show_table.data:
    #             report_param += " --info"
    #         os.system("python " +
    #                   __file__.replace("web/app/routes.py", "main.py") +
    #                   report_param)
    #         return send_file(__file__.replace("web/app/routes.py", "data/report.pdf"), attachment_filename="report.pdf")
    # Достаем данные о заправлках из базы данных
    logger.debug("Selecting data from trans view")
    trans_data = db.select("vtrans",
                           "id, fuel_id, dtime, odometer, name, amount",
                           order_by="dtime")
    logger.debug("Selecting data from fuel view")
    fuel_data = db.select("vfuel", "id, name, price")

    # Обновляем страницу
    logger.debug("Rendering index page")
    return render_template("index.html",
                           trans_data=trans_data,
                           fuel_data=fuel_data,
                           navig_trans_form=navig_trans_form,
                           navig_fuel_form=navig_fuel_form,
                           trans_row_form=trans_row_form,
                           trans_new_row_form=trans_new_row_form,
                           fuel_row_form=fuel_row_form,
                           fuel_new_row_form=fuel_new_row_form,
                           report_form=report_form,
                           table_name=table_name)



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
        return redirect(url_for('index'))
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
