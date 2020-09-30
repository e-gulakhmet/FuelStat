import logging
import database
# from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer, Frame, PageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


# TODO: Добавить в таблицу данные о цене одного дня и пробеге между заправками
# TODO: Добавить статистику по выгодности заправок
# TODO: Добавить информацию о самой часто используемой заправке
# TODO: Добавить информацию о среднем расходе



def report(start_date=None, end_date=None, gas_names=None, file_name=None):
    logger = logging.getLogger("REPORT")  
    logger.debug("Report parameters: start_date[" + str(start_date) + ']' +
                 ", end_date[" + str(end_date) + ']' +
                 ", gas_names[" + str(gas_names) + ']' +
                 ", file_name[" + str(file_name) + ']')
    
    db = database.DataBase("data/database.db")
    
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
                      f.price as gallon_price,
                      t.amount,
                      t.amount * f.price / 100 as cost,
                      (t.odometer - tt.odometer) / t.amount as mpg,
                      t.amount * f.price / (t.odometer - tt.odometer) as mile_price""",
                   """t.fuel_id = f.id 
                      AND tt.id = (SELECT MAX(id) FROM trans WHERE id < t.id)
                      ORDER BY t.dtime""")


    # Получаем данные для таблицы из базы дыннах
    # Создаем строку условия для select
    condition = ""
    if start_date is not None:
        condition = "dtime >= '" + str(start_date) + "'"
    else:
        condition = "dtime >= '1000-00-00'"
    if end_date is not None:
        condition += " AND dtime <= '" + str(end_date) + "'"
    if gas_names is not None:
        condition += " AND name in " + str(tuple(gas_names))

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
    s_header = styles["Heading1"]
    s_header.alignment = TA_CENTER

    s_param = styles["Normal"]
    s_param.fontSize = 12
    s_param.spaceAfter = 10

    # Рисование на документе
    # frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
    #               id='normal')
    # template = PageTemplate(id='test', frames=frame, onPage=footer)
    # doc.addPageTemplates([template])

    # Название документа
    elements.append(Paragraph("FuelStatReport", s_header))
    elements.append(Spacer(0, 20))
    
    # Параметры отчета
    elements.append(Paragraph("Start Date: " + start_date, s_param))
    elements.append(Paragraph("End Date: " + end_date, s_param))
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
    elements.append(Paragraph("Gas Stations: " + gs, s_param))
    elements.append(Spacer(0, 20))

    # Получаем данные из базы данных
    table_data = table_data_to_list(db.select("v_trans", 
                                              """dtime, name,
                                                 odometer, gallon_price,
                                                 amount, cost, mpg,
                                                 mile_price""",
                                              condition))
    table_data.insert(0,
                      ["DATE", "GAS", "ODOMETER", "GALLON \n PRICE",
                       "GALLONS", "COST", "MPG", "MILE \n PRICE"])

    # Создаем таблицу
    t = Table(table_data, repeatRows=True)
    t.setStyle(TableStyle([
                          ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                          ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                          ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
                          ]))
    
    elements.append(t)
    
    doc.build(elements)

    # pdf = canvas.Canvas("data/" + file_name + ".pdf", A4)

    # # Рисуем заголовок
    # pdf.drawString(82 * mm, h - 8.4 * mm, "FuelStat Report")
    
    # # Рисуем параметры полученной таблицы
    # pdf.drawString(8 * mm, h - 29 * mm, "Start Date: " + start_date)
    # pdf.drawString(60 * mm, h - 29 * mm, "End Date: " + end_date)
    # gs = ""
    # # Создаем строку с названями заправки
    # if gas_names is None:
    #     gs = "All"
    # else:
    #     gs = str(gas_names[0])
    #     for n in gas_names:
    #         gs += ", " + str(n)
    # # Выводим созданную строку
    # pdf.drawString(110 * mm, h - 29 * mm, "Gas Stations: " + gs)

    # pdf.setLineWidth(1 * mm)
    # pdf.line(8 * mm, h - 35 * mm, 200 * mm, h - 35 * mm)

    # # Создаем таблицу
    # # Получаем данные из базы данных
    # table_data = table_data_to_list(db.select("v_trans", 
    #                                           """dtime, name,
    #                                              odometer, gallon_price,
    #                                              amount, cost, mpg,
    #                                              mile_price""",
    #                                           condition))
    # table_data.insert(0, 
    #                   ["DATE", "GAS", "ODOMETER", "GALLON \n PRICE",
    #                    "GALLONS", "COST", "MPG", "MILE \n PRICE"])
    # # Проверяем, если данные слишком много,
    # # то переносим оставшиеся данные на следующую страницу
    # t = Table(table_data, repeatRows=1)
    # t_w, t_h = t.wrap(0, 0)
    # t.wrapOn(pdf, w, h)
    # t.setStyle(TableStyle([
    #     ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
    #     ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    #     ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
    # ]))
    # # Выводим таблицу
    # t.drawOn(pdf, 9 * mm, h - 42 * mm - t_h)

    # pdf.showPage()

    # pdf.drawString(0, 0, "Hello")

    # pdf.save()
    # logger.info("Report was saved")


def table_data_to_list(data):
    c = []
    for row in data:
        lst = []
        for e in row:
            if type(e) is float:
                e = "%.1f" % e
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
