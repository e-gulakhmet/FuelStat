# Модуль содержущий в себе функции испольняемые в routes
import os
from app import flsk
import re


def update_file(upload_file_data, path_to_old_file: str, file_type: str, logger):
    """
    Добавляет данные нового файла в уже имеющийся файл.
    """
    path = os.path.join(flsk.config["UPLOAD_FOLDER"], upload_file_data.filename)
    logger.debug("Saving file:" + str(upload_file_data.filename))
    upload_file_data.save(path)
    logger.info(str(upload_file_data.filename) +
                "file was saved")
    # Добавяляем данные из нового файла в уже имеющийся
    logger.debug("Updating " + path_to_old_file)
    with open(path, "r") as new_file:
        with open(path_to_old_file, "a") as update_file:
            for line in new_file.readlines():
                if file_type == "fuel":
                    if re.search("^[A-Z].*[,]*\d$", line):
                        update_file.write(line)
                        continue
                elif file_type == "trans":
                    if re.search("^\d{4}-\d{2}-\d{2},\d*,[A-Za-z]*,\d", line):
                        update_file.write(line)
                        continue
                logger.warning("Invalid row in " + line + ", " + str(upload_file_data.filename))
    logger.info(path_to_old_file + "was updated by " + str(upload_file_data.filename))
    # Удаляем сохраненный файл
    os.remove(path)


def replace_file(upload_file_data, path_to_old_file, file_type, logger):
    # Сохраняем новый файл с название как у старого(fuel.csv)
    # Тем самым заменяя его
    logger.debug("Replacing " + path_to_old_file +
                 " data on " + str(upload_file_data.filename) +
                 " data")
    path = os.path.join(flsk.config["UPLOAD_FOLDER"], upload_file_data.filename)
    logger.debug("Saving file:" + str(upload_file_data.filename))
    upload_file_data.save(path)
    logger.info(str(upload_file_data.filename) +
                "file was saved")
    # Проверяем данные из нового файла
    logger.debug("Checking " + str(upload_file_data.filename))
    with open(path, "r") as new_file:
        with open(path_to_old_file, "w") as replace_file:
            for line in new_file.readlines():
                if file_type == "fuel":
                    if re.search("^[A-Z].*[,]*\d$", line):
                        continue
                elif file_type == "trans":
                    if re.search("^\d{4}-\d{2}-\d{2},\d*,[A-Za-z]*,\d", line):
                        continue
                os.remove(path)
                logger.warning("Invalid row in " + line + ", " + str(upload_file_data.filename))
                logger.warning("File was not replaced")
                return
            replace_file.write(new_file)
    logger.info(path_to_old_file + "was replaced by " + str(upload_file_data.filename))


def create_report(path_to_report_gen_file: str,
                  start_date: str, end_date: str,
                  start_odometer: str, end_odometer: str,
                  names: list,
                  statistic: bool, table: bool,
                  stations_info: list, logger):
    """
    Запускает скрипт, который создаст отчет с
    указанными параметрами.
    """
    report_param = (" --report" +
                    " --startdate " + start_date +
                    " --enddate " + end_date +
                    " --startodometer " + start_odometer +
                    " --endodometer " + end_odometer)
    if names is not None:
        for i in names:
            for station in stations_info:
                if station[0] == i:
                    report_param += " --gasname " + station[1]
                    break
    if statistic:
        report_param += " --statistic"
    if table:
        report_param += " --info"
    os.system("python " + path_to_report_gen_file +
              report_param)
    logger.info("Generate report was sent")
