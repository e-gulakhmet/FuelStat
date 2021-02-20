import os


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