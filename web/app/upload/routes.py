# Данные файл содержит в себе функции для отображения страниц, по
# указанным путям

from flask import render_template
from flask_login import login_required
import logging
import os

from app import flsk
from app.upload import bp 
from app.upload.forms import UploadFuelForm, UploadTransForm
from app.upload.funcs import update_file, replace_file



@bp.route("/upload", methods=["GET", "POST"])
@login_required # Проверяем авторизовался ли пользователь
def upload():
    logger = logging.getLogger("UPLOAD")
    upload_trans_form = UploadTransForm()
    upload_fuel_form = UploadFuelForm()

    if upload_fuel_form.validate_on_submit() and upload_fuel_form.upload_fuel.data:
        logger.debug("Upload fuel form button was pressed")
        # Если был выбран метод добавление данных файлв к уже имеющимся
        path_to_old_file = os.path.join(flsk.config["DATA_FOLDER"], "fuel.csv")
        if upload_fuel_form.method_fuel.data == "0":
            update_file(upload_fuel_form.file_fuel.data, path_to_old_file,
                        "^[A-Z].*[,]*\d$", logger)
        # Если был выбран режим замены старого файла новым
        elif upload_fuel_form.method_fuel.data == "1":
            replace_file(upload_fuel_form.file_fuel.data,
                         path_to_old_file, "^[A-Z].*[,]*\d$",
                         logger)
    
    if upload_trans_form.validate_on_submit() and upload_trans_form.upload_trans.data:
        logger.debug("Upload trans form button was pressed")
        # Если был выбран метод добавление данных файлв к уже имеющимся
        path_to_old_file = os.path.join(flsk.config["DATA_FOLDER"], "trans.csv")
        if upload_trans_form.method_trans.data == "0":
            update_file(upload_trans_form.file_trans.data,
                        path_to_old_file,
                        "^\d{4}-\d{2}-\d{2},\d*,[A-Za-z]*,\d", logger)
        # Если был выбран режим замены старого файла новым
        elif upload_trans_form.method_trans.data == "1":
            replace_file(upload_trans_form.file_trans.data,
                         path_to_old_file,
                         "^\d{4}-\d{2}-\d{2},\d*,[A-Za-z]*,\d", logger)
        
        # Говорим программе, которая создает репорт, обновить базу данных
        os.system("python " +
                  os.path.join(flsk.config["FUELSTAT_FOLDER"], "main.py") +
                  " --load --recreate")

    return render_template("upload.html",
                           upload_trans_form=upload_trans_form,
                           upload_fuel_form=upload_fuel_form)