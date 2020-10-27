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
# TODO: Добавить значения в ячейки цены дня, сумму цен заправок этого дня



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
    condition = """t.fuel_id = f.id AND tt.id = (SELECT MAX(id) FROM trans WHERE id < t.id)
                   AND nt.id = (SELECT MIN(id) FROM trans WHERE id > t.id)"""
    if start_date is not None:
        condition += " AND t.dtime >= '" + str(start_date) + "'"
    if end_date is not None:
        condition += " AND t.dtime <= '" + str(end_date) + "'"
    if gas_names is not None:
        condition += " AND f.name in " + str(tuple(gas_names))
    condition += " ORDER BY t.dtime"
    
    # Данные, получаемые из таблицы:
    # id, дата, название заправки,
    # расстояние пройденное до текущего дня,
    # расстояние проеденное до предыдущего дня,
    # цена галлона,
    # количество галлонов,
    # цена заправки,
    # пробег на одном галлоне,
    # стоимость одной милю,
    # пробег между заправками,
    # стоимость одного дня
    db.create_view("v_trans",
                   "trans t, trans tt, trans nt, fuel f",
                   """t.id, t.dtime,
                      nt.dtime as next_dtime,
                      tt.dtime as prev_dtime,
                      f.name,
                      t.odometer,
                      tt.odometer as last_odometer,
                      t.odometer - tt.odometer as mbs,
                      f.price as gallon_price,
                      t.amount,
                      t.amount * f.price / 100 as cost,
                      (t.odometer - tt.odometer) / t.amount as mpg,
                      t.amount * f.price / (t.odometer - tt.odometer) as mile_price
                      """,
                   condition,
                   True)

    # Создаем pdf файл
    w, h = A4 # Размер листа

    # Cоздаем документ, в котором будут содержать полученные данные
    doc = SimpleDocTemplate("data/" + file_name + ".pdf",
                            pagesize=A4,
                            topMargin=5 * mm,
                            bottomMargin=5 * mm,
                            leftMargin=10 * mm,
                            rightMargin=10 * mm,
                            showBoundary=0)
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
    # elements.append(Paragraph("Gas Stations: " + gs, s_param))
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
    table_data = table_data_to_list(db.select("v_trans", 
                                              """dtime, name,
                                                 odometer, mbs, gallon_price,
                                                 amount, cost, mpg,
                                                 mile_price,
                                                 CASE next_dtime = dtime
                                                    WHEN FALSE
                                                        THEN (SELECT SUM(cost) FROM v_trans GROUP BY dtime)
                                                END
                                                 """))

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

    print(merge_rows)

    # Добваление цены одного дня в таблицу:
    # Проверяем дату заправки
    # merge_rows = []
    # merging = False
    # cost = 0
    # for i in range(1, len(table_data)):
    #     # Если дата текущей равна дате первой заправки
    #     # или дата текущей заправки равна дате предыдущей заправки
    #     if table_data[i][0] == table_data[1][0] or table_data[i][0] == table_data[i - 1][0]:
    #         # Добавляем цену заправки к сумме
    #         cost += float(table_data[i][6])             
    #         if merging is False:
    #             if table_data[i][0] == table_data[1][0]:
    #                 merge_rows.append([i, ])
    #             else:
    #                 merge_rows.append([i - 1, ])
    #             merging = True
    #     else:
    #         if len(merge_rows) != 0 and merging is True:
    #             if table_data[i][0] == table_data[len(table_data) - 1][0]:
    #                 table_data[merge_rows[len(merge_rows) - 1][0]].append(cost + table_data[i][6])
    #                 merge_rows[len(merge_rows) - 1].append(i)
    #             else:
    #                 table_data[merge_rows[len(merge_rows) - 1][0]].append(cost)
    #                 merge_rows[len(merge_rows) - 1].append(i - 1)
    #             merging = False
    #         else:
    #             table_data[i - 1].append(cost)
    #         cost = float(table_data[i][6])
    # print(merge_rows)



    # Создаем таблицу
    main_table = Table(table_data, repeatRows=True)
    table_style = [("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                   ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]
    for row in merge_rows:
        table_style.append(("SPAN", (9, row[0]), (9, row[1])))

    main_table.setStyle(TableStyle(table_style))
    elements.append(main_table)
    elements.append(Spacer(0, 20))

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