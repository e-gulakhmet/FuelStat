import logging
import database



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
                  """t.id, t.dtime, f.name, f.price, t.odometer,
                     tt.odometer, t.amount, (t.odometer - tt.odometer) / t.amount AS cons,
                     t.amount * f.price / 100 AS cost""",
                  condition)
    logger.info("Report data was selected from database")
    
    for row in c:
        print(row)
    print("\n")