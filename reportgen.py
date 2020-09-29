import logging
import database
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle



# TODO: Сделать переход на следующую страницу, если данных слишком много
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

    logger.info("Report data was selected from database")

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
    pdf = canvas.Canvas("data/" + file_name + ".pdf", A4)

    # Рисуем заголовок
    pdf.drawString(82 * mm, h - 8.4 * mm, "FuelStat Report")
    
    # Рисуем параметры полученной таблицы
    pdf.drawString(8 * mm, h - 29 * mm, "Start Date: " + start_date)
    pdf.drawString(60 * mm, h - 29 * mm, "End Date: " + end_date)
    gs = ""
    # Создаем строку с названями заправки
    if gas_names is None:
        gs = "All"
    else:
        gs = str(gas_names[0])
        for n in gas_names:
            gs += ", " + str(n)
    # Выводим созданную строку
    pdf.drawString(110 * mm, h - 29 * mm, "Gas Stations: " + gs)

    pdf.setLineWidth(1 * mm)
    pdf.line(8 * mm, h - 35 * mm, 200 * mm, h - 35 * mm)

    # Создаем таблицу
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
    t = Table(table_data)
    t_w, t_h = t.wrap(0, 0)
    t.wrapOn(pdf, w, h)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
    ]))
    # Выводим таблицу
    t.drawOn(pdf, 9 * mm, h - 42 * mm - t_h)

    pdf.showPage()

    pdf.drawString(0, 0, "Hello")

    pdf.save()
    logger.info("Report was saved")


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