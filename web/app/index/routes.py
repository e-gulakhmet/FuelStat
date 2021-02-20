from flask import render_template, request, send_file
from flask_login import login_required
import logging
import os

from app import flsk
from app.index import bp
from app.database import DataBase
from app.index.forms import NavigationTransForm, NavigationFuelForm
from app.index.forms import TransTableRowForm, TransTableNewRowForm
from app.index.forms import FuelTableNewRowForm, FuelTableRowForm, ReportForm
from app.index.funcs import create_report



@bp.route("/index", methods=["GET", "POST"])
@login_required # Проверяем авторизовался ли пользователь
def index():
    logger = logging.getLogger("INDEX")
    
    db = DataBase(os.path.join(flsk.config["FUELSTAT_FOLDER"], "data/database.db"))
    stations_info = list(db.select("fuel", "CAST(id as TEXT), name"))

    navig_trans_form = NavigationTransForm()
    navig_trans_form.names_trans_navigation.choices = stations_info

    navig_fuel_form = NavigationFuelForm()

    trans_row_form = TransTableRowForm()

    trans_new_row_form = TransTableNewRowForm()

    fuel_row_form = FuelTableRowForm()

    fuel_new_row_form = FuelTableNewRowForm()

    report_form = ReportForm()
    report_form.names_report.choices = stations_info

    table_name = "trans"

    # Создаем view для того, чтобы в дальнейшем не повторять условия 
    db.create_view("vtrans", "trans t, fuel f",
                   "t.id, t.fuel_id, t.dtime, t.odometer, f.name, t.amount",
                   "t.fuel_id = f.id", "t.dtime", re_create=True)
    db.create_view("vfuel", "fuel", "id, name, price", re_create=True)

    if request.method == "POST":
        # Проверяем, была ли нажата какая-то из submit кнопок в веб формах
        if navig_trans_form.validate() and navig_trans_form.allow_trans_navigation.data:
            # Если кнопка подтвержедения в навигационной форме была нажата,
            # то Создаем новую view
            logger.debug("Allow button was pressed in the trans navigation")
            condition = ("t.fuel_id = f.id" +
                         (" AND t.dtime > '" +
                          str(navig_trans_form.start_date_trans_navigation.data) + "'" +
                          " AND t.dtime < '" +
                          str(navig_trans_form.end_date_trans_navigation.data) + "'" +
                          " AND t.odometer > " +
                          str(navig_trans_form.start_odometer_trans_navigation.data) +
                          " AND t.odometer < " +
                          str(navig_trans_form.end_odometer_trans_navigation.data)))
            if len(navig_trans_form.names_trans_navigation.data) == 1:
                condition += (" AND t.fuel_id == " +
                              str(navig_trans_form.names_trans_navigation.data[0]))
            elif len(navig_trans_form.names_trans_navigation.data) != 0:
                condition += (" AND t.fuel_id in " +
                              str(tuple(navig_trans_form.names_trans_navigation.data)))
            db.create_view("vtrans", "trans t, fuel f",
                           "t.id,  t.fuel_id, t.dtime, t.odometer, f.name, t.amount",
                           condition, "dtime", re_create=True)
            db.commit()
            table_name = "trans"

        elif navig_fuel_form.validate() and navig_fuel_form.allow_fuel_navigation.data:
            # Если кнопка подтвержедения в навигационной форму была нажата,
            # то создаем новую view
            logger.debug("Allow button was pressed in the fuel navigation")
            db.create_view("vfuel", "fuel", "id, name, price",
                           ("price > " +
                            str(navig_fuel_form.start_price_fuel_navigation.data) +
                            " AND price < " +
                            str(navig_fuel_form.end_price_fuel_navigation.data)),
                           re_create=True)
            db.commit()
            table_name = "fuel"

        elif trans_row_form.validate() and (trans_row_form.save_trans_row.data or trans_row_form.delete_trans_row.data):
            if trans_row_form.save_trans_row.data:
                # Если кнопка сохранения была нажата, то обновляем
                # уже имеющуюся строку в таблице,
                # подстваляя новые значения
                logger.debug("Save button was pressed in the row of the trans table")
                db.update("trans", 
                          ("dtime = '" +
                           str(trans_row_form.date_trans_row.data) + "'" +
                           ", odometer = " +
                           str(trans_row_form.odometer_trans_row.data) +
                           ", fuel_id = " +
                           str(trans_row_form.fuel_station_trans_row.data) +
                           ", amount = " +
                           str(trans_row_form.gallon_count_trans_row.data)),
                          "id = " + str(trans_row_form.id_trans_row.data))
                db.commit()
                table_name = "trans"
            elif trans_row_form.delete_trans_row.data:
                # Если была нажата кнопка удаления в веб форме строки в таблицу,
                # то удаляем строку в которой id из таблицы будет совподать с id из веб формы
                logger.debug("Delete button was pressed in the row of the trans table")
                db.delete("trans", "id = " + str(trans_row_form.id_trans_row.data))
                db.commit()
                table_name = "trans"
        
        elif fuel_row_form.validate() and (fuel_row_form.save_fuel_row.data or fuel_row_form.delete_fuel_row.data):
            if fuel_row_form.save_fuel_row.data:
                # Если кнопка сохранения была нажата, то обновляем уже имеющуюся строку в таблице,
                # подстваляя новые значения
                logger.debug("Save button was pressed in the row of the fuel table")
                db.update("fuel",
                          ("name = '" + str(fuel_row_form.name_fuel_row.data) + "'" +
                           ", price = " + str(fuel_row_form.price_fuel_row.data)),
                          "id = " + str(fuel_row_form.id_fuel_row.data))
                db.commit()
                table_name = "fuel"
            elif fuel_row_form.delete_fuel_row.data:
                # Если была нажата кнопка удаления в веб форме строки в таблицу,
                # то удаляем строку в которой id из таблицы будет совподать с id из веб формы
                logger.debug("Delete button was pressed in the row of the fuel table")
                if str(fuel_row_form.id_fuel_row.data) != "-1":
                    db.delete("fuel", "id = " + str(fuel_row_form.id_fuel_row.data))
                    db.commit()
                table_name = "fuel"
        
        elif trans_new_row_form.validate() and trans_new_row_form.add_trans_new_row.data:
            # Если в веб форме новой строки, была нажата кнопка добавления,
            # добавляем новую строку с параментрами из веб форм
            logger.debug("Add button was pressed in the new row of the trans table")
            db.insert("trans", "dtime, odometer, fuel_id, amount",
                      ("'" + str(trans_new_row_form.date_trans_new_row.data) + "'" +
                       ", " + str(trans_new_row_form.odometer_trans_new_row.data) + 
                       ", " + str(trans_new_row_form.fuel_station_trans_new_row.data) +
                       ", " + str(trans_new_row_form.gallon_count_trans_new_row.data)))
            db.commit()
            table_name = "trans"
        
        elif fuel_new_row_form.validate() and fuel_new_row_form.add_fuel_new_row.data:
            # Если в веб форме новой строки, была нажата кнопка добавления,
            # добавляем новую строку с параментрами из веб форм
            logger.debug("Add button was pressed in the new row of the fuel table")
            db.insert("fuel", "name, price", 
                      ("'" + str(fuel_new_row_form.name_fuel_new_row.data) + "'" +
                       ", " + str(fuel_new_row_form.price_fuel_new_row.data)))
            db.commit()
            table_name = "fuel"
        
        elif report_form.validate() and report_form.get_report.data:
            # Если кнопка подтвержедения в навигационной форме была нажата,
            # то Создаем новую view
            logger.debug("Allow button was pressed in the report")
            create_report(os.path.join(flsk.config["FUELSTAT_FOLDER"], "main.py"),
                          str(report_form.start_date_report.data),
                          str(report_form.end_date_report.data),
                          str(report_form.start_odometer_report.data),
                          str(report_form.end_odometer_report.data),
                          str(report_form.names_report.data),
                          report_form.show_statistic_report.data,
                          report_form.show_table_report.data,
                          stations_info, logger)
            return send_file(os.path.join(flsk.config["FUELSTAT_FOLDER"],
                                          "data/report.pdf"),
                             attachment_filename="report.pdf")

    # Достаем данные о заправлках из базы данных
    logger.debug("Selecting data from trans view")
    trans_data = db.select("vtrans",
                           "id, fuel_id, dtime, odometer, name, amount",
                           order_by="odometer")
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
