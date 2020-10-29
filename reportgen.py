import logging
import database
# from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer, Flowable
from reportlab.lib.styles import getSampleStyleSheet


# TODO: Добавить статистику



class MyLine(Flowable):
    """
    Custom line for DocTemplate
    """

    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
    
    def draw(self):
        self.canv.line(0, self.height, self.width, self.height)



def report(start_date=None, end_date=None, gas_names=None, file_name=None):
    logger = logging.getLogger("REPORT")  
    logger.debug("Report parameters: start_date[" + str(start_date) + ']' +
                 ", end_date[" + str(end_date) + ']' +
                 ", gas_names[" + str(gas_names) + ']' +
                 ", file_name[" + str(file_name) + ']')
    
    db = database.DataBase("data/database.db")

    # Создаем строку условия для select
    logger.debug("Creating data base condition")
    condition = ""
    if start_date is not None:
        condition = upd_condition(condition, "dtime >= '" + str(start_date) + "'")
    if end_date is not None:
        condition = upd_condition(condition, "dtime <= '" + str(end_date) + "'")
    if gas_names is not None:
        condition = upd_condition(condition, "name in " + str(tuple(gas_names)))
    logger.debug("Conditions is + " + condition)
    logger.info("Condition was created")

    # Создаем pdf файл
    w, h = A4 # Размер листа

    # Cоздаем документ, в котором будут содержать полученные данные
    logger.debug("Creating DocTemplate")
    doc = SimpleDocTemplate("data/" + file_name + ".pdf",
                            pagesize=A4,
                            topMargin=5 * mm,
                            bottomMargin=5 * mm,
                            leftMargin=10 * mm,
                            rightMargin=10 * mm,
                            showBoundary=0)
    logger.info("DocTemplate was created")

    logger.info("Creating document's elements")
    elements = [] # Список, который будет содержать все элементы документа
    styles = getSampleStyleSheet()
    # Создаем нужные нам стили
    s_header_1 = styles["Heading1"]
    s_header_1.alignment = TA_CENTER
    s_param = styles["Normal"]
    s_param.fontSize = 12
    s_param.spaceAfter = 10
    s_header_2 = styles["Heading1"]
    s_header_2.alignment = TA_CENTER

    # Название документа
    elements.append(Paragraph("FuelStatReport", s_header_1))
    elements.append(Spacer(0, 20))
    
    # Параметры отчета
    param_info = "Start Date: " + start_date 
    param_info += "&nbsp;&nbsp;&nbsp;&nbsp; End Date: " + end_date
    gs = ""
    # Создаем строку с названями заправки
    if gas_names is None:
        gs = "All"
    else:
        gs = str(gas_names[0])
        for n in gas_names:
            gs += ", " + str(n)
    # # Выводим созданную строку
    # parameters += "    Gas Stations: " + gs
    param_info += "&nbsp;&nbsp;&nbsp;&nbsp; Gas Stations: " + gs
    elements.append(Paragraph(param_info, s_param))

    # Рисуем линию после параметров отчета
    elements.append(MyLine(doc.width, 0))
    elements.append(Spacer(0, 20))

    # Получаем данные из базы данных
    # Условия получения информации из вьюшки для цены дня:
    # Если дата текущей заправки равна дате предыдущей заправки,
    # то прибавляем ее цену к сумме.
    # Если даты разные, то сохраняем сумму в предыдущую заправку, затем
    # сумму приравниваем к цене текущей запраки.
    table_data = table_data_to_list(db.select("v_trans vv", 
                                              """dtime, name,
                                                 odometer, mbs, gallon_price,
                                                 amount, cost, mpg,
                                                 mile_price,
                                                 CASE next_dtime = dtime
                                                    WHEN FALSE
                                                        THEN (SELECT SUM(v.cost) FROM v_trans v WHERE v.dtime = vv.dtime GROUP BY v.dtime)
                                                 END
                                              """,
                                              condition + " ORDER BY dtime"))

    table_data.insert(0,
                      ["DATE", "GAS", "ODOMETER",
                       "MILIAGE \n BEETWEEN", "GALLON \n PRICE",
                       "GALLONS", "COST", "MPG", "MILE \n PRICE", "DAY \n PRICE"])


    # После получения данных из вьюшки нужно создать список,
    # в котором будут хранится строки,
    # которые нужно объединить объединить в таблице.
    # Элемент списка будет выглядить вот так: [s_cell, e_cell]
    merge_rows = []
    merging = False
    # В списке, который мы получили от базы данны, проверяем:
    logger.debug("Creating merging rows list for document's table")
    for i in range(1, len(table_data)):
        # Если ячейка цены дня пустая и флажок объединения не активен:
        if table_data[i][9] is None and merging is False:
            # Записываем текущую строку, как начальную для объединения и
            # активируем флажок объединения.
            merge_rows.append([i, ])
            merging = True
        # Если ячейка цены дня не пустая и флажок объединения активен,
        elif table_data[i][9] is not None and merging is True:
            # то указываем текущую ячейку, как конечную для объединения и
            # выключаем флажок объединения.
            table_data[merge_rows[len(merge_rows) - 1][0]][9] = table_data[i][9]
            merge_rows[len(merge_rows) - 1].append(i)
            merging = False
    logger.debug("Merging rows is " + str(merge_rows))
    logger.info("Merging rows list was created")


    # Создаем таблицу
    logger.debug("Creating document's table")
    try:
        main_table = Table(table_data, repeatRows=True)
        table_style = [("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                       ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]
        for row in merge_rows:
            table_style.append(("SPAN", (9, row[0]), (9, row[1])))
        main_table.setStyle(TableStyle(table_style))
    except IndexError:
        logger.error("Table data is empty or unsupported")
    logger.info("Document's table was created")
    elements.append(main_table)
    elements.append(Spacer(0, 20))

    # Получаем данные по статистике из вьюшки
    # - Общее пройденное расстояние(мили).
    # - Общая стомость заправок(доллары).
    # - Средний расход топлива(галлоны).
    # - Средний пробег(мили).
    # - Средняя цена одной заправки(доллары).
    # - Средний пробег на одном галлоне(мили).
    # - Средняя цена одной мили(доллары).
    # - Самая часто посещаемая вами заправка.
    # - Самая выгодная заправка и информация о ней.
    # - Количество долларов, которые можно было сэкономить,
    #   если заправляться только на самой выгодной заправке.
    table_data = table_data_to_list(db.select("v_trans",
                                              """
                                                MAX(odometer) - MIN(odometer),
                                                SUM(cost),
                                                SUM(amount) / (MAX(odometer) - MIN(odometer)) * 60
                                              """,
                                              condition))
    print(table_data)


    doc.build(elements)


def table_data_to_list(data):
    c = []
    for row in data:
        lst = []
        for e in row:
            if type(e) is float:
                e = round(e, 2)
            lst.append(e)
        c.append(lst)
    return c


def upd_condition(source, addition):    
    if source == "":
        source = addition
    else:
        source += " AND " + addition

    return source