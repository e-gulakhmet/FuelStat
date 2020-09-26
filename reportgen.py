import logging
import database
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4 



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
    # Объединяем данные из таблиц
    c = db.select("trans t, trans tt, fuel f",
                  # Данные, получаемые из таблицы:
                  # id, дата, название заправки,
                  # расстояние пройденное до текущего дня,
                  # расстояние проеденное до предыдущего дня,
                  # цена галлона,
                  # количество галлонов,
                  # цена заправки,
                  # пробег между заправками,
                  # пробег на одном галлоне,
                  # стоимость пробега в одну милю,
                  # стоимость одного дня
                  """t.id, t.dtime, f.name,
                     t.odometer,
                     tt.odometer,
                     f.price,
                     t.amount,
                     t.amount * f.price / 100,
                     t.odometer - tt.odometer,
                     (t.odometer - tt.odometer) / t.amount,
                     t.amount / (t.odometer - tt.odometer),
                     t.amount / (t.odometer - tt.odometer)
                     """,
                  condition)
    logger.info("Report data was selected from database")

    for row in c:
        print(row)
    print("\n")

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

    

    pdf.save()