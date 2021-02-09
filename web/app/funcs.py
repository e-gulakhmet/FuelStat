# Модуль содержущий в себе функции испольняемые в routes
import os
from app import flsk


def update_file(upload_file_data, path_to_old_file: str, logger):
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
        new_file = '\n' + new_file.read()
        with open(path_to_old_file, "a") as update_file:
            update_file.write(new_file)
    logger.info(path_to_old_file + "was updated by " + str(upload_file_data.filename))
    # Удаляем сохраненный файл
    os.remove(path)


def replace_file(upload_file_data, path_to_old_file, logger):
    # Сохраняем новый файл с название как у старого(fuel.csv)
    # Тем самым заменяя его
    logger.debug("Replacing " + path_to_old_file +
                 " data on " + str(upload_file_data.filename) +
                 " data")
    upload_file_data.save(path_to_old_file)
    logger.info(str(upload_file_data.filename) +
                "file was saved")


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
