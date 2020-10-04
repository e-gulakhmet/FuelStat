import logging
import database
# from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer, Flowable
from reportlab.lib.styles import getSampleStyleSheet


# TODO: Добавить в таблицу данные о цене одного дня
# TODO: Добавить статистику по выгодности заправок
# TODO: Добавить информацию о самой часто используемой заправке
# TODO: Добавить информацию о среднем расходе
# TODO: Сделать перенос таблицы(маленькая) в правую сторону



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
    condition = "t.fuel_id = f.id AND tt.id = (SELECT MAX(id) FROM trans WHERE id < t.id)"
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
                   "trans t, trans tt, fuel f",
                   """t.id, t.dtime, f.name,
                      t.odometer,
                      tt.odometer as last_odometer,
                      t.odometer - tt.odometer as mbs,
                      f.price as gallon_price,
                      t.amount,
                      t.amount * f.price / 100 as cost,
                      (t.odometer - tt.odometer) / t.amount as mpg,
                      t.amount * f.price / (t.odometer - tt.odometer) as mile_price""",
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

    # Рисование на документе
    # frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
    #               id='normal')
    # template = PageTemplate(id='test', frames=frame, onPage=footer)
    # doc.addPageTemplates([template])

    # Название документа
    elements.append(Paragraph("FuelStatReport", s_header_1))
    elements.append(Spacer(0, 20))
    
    # Параметры отчета
    param_info = "Start Date: " + start_date 
    param_info += "&nbsp;&nbsp;&nbsp;&nbsp; End Date: " + end_date
    # elements.append(Paragraph("Start Date: " + start_date, s_param))
    # elements.append(Paragraph("End Date: " + end_date, s_param))
    # parameters = "Start Date: " + start_date + "    End Date: " + end_date
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
    elements.append(Paragraph("Information about gas stations", s_header_2))
    # Получаем данные из базы данных
    table_data = table_data_to_list(db.select("v_trans", 
                                              """dtime, name,
                                                 odometer, mbs, gallon_price,
                                                 amount, cost, mpg,
                                                 mile_price"""))
    table_data.insert(0,
                      ["DATE", "GAS", "ODOMETER",
                       "MILIAGE \n BEETWEEN", "GALLON \n PRICE",
                       "GALLONS", "COST", "MPG", "MILE \n PRICE"])

    # Создаем таблицу
    main_table = Table(table_data, repeatRows=True)
    main_table.setStyle(TableStyle([
                                   ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                   ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
                                   ]))
    elements.append(main_table)
    elements.append(Spacer(0, 20))

    # Формируем таблицу
    elements.append(Paragraph("Information about gas stations", s_header_2))
    # Цена одного дня:
    # Проверяем дату заправки
    data = table_data_to_list(db.select("v_trans", "dtime, cost"))
    table_data.clear()
    cost = 0
    date = data[0][0]
    for day in data:
        if day[0] == date or day[0] == data[0][0]:
            cost += float(day[1])
            continue
        else:
            table_data.append([date, cost])
            date = day[0]
            cost = float(day[1])
    days_table1 = Table(table_data[:int((len(data) - 1) / 4)], repeatRows=True)
    days_table1.setStyle(TableStyle([
                                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
                                    ]))
    days_table2 = Table(table_data[int((len(data) - 1) / 4):2 * int((len(data) - 1) / 4)], repeatRows=True)
    days_table2.setStyle(TableStyle([
                                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
                                    ]))
    days_table3 = Table(table_data[2 * int((len(data) - 1) / 4):3 * int((len(data) - 1) / 4)], repeatRows=True)
    days_table3.setStyle(TableStyle([
                                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
                                    ]))
    days_table4 = Table(table_data[3 * int((len(data) - 1) / 4):], repeatRows=True)
    days_table4.setStyle(TableStyle([
                                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
                                    ]))

    days_table = Table([[days_table1, days_table2, days_table3, days_table4]])
                                   
    elements.append(days_table)
    # Сохраняем дату и добавляем к сумме цену заправки
    # переходим к следующей
    # Если числа разные, то сохраняем дату и сумму в список
    # затем обнуляем ее 
    # Иначе добавляем цену заправки к сумме и переходим к следующей заправке


   
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


# def footer(canvas, doc): # Функция позволяющая рисовать на документе
#     styles = getSampleStyleSheet()
#     canvas.saveState()
#     # P = Paragraph("FuelStat", styles["Heading1"])

#     # w, h = P.wrap(doc.width, doc.bottomMargin)
#     # P.drawOn(canvas, doc.leftMargin, h)

#     # .drawString(8 * mm, h - 29 * mm, "Start Date: " + start_date)
#     # pdf.drawString(60 * mm, h - 29 * mm, "End Date: " + end_date)
#     # canvas.restoreState()
