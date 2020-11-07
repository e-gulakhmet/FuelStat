# from reportlab.pdfgen import canvas
import logging
import argparse

import database
import reporter


# TODO: Добавить русский язык


def main():
    parser = argparse.ArgumentParser(prog="fuel_stat",
                                     description="""Creating statistics 
                                                    based on generated tables""")
    parser.add_argument("--recreate", action="store_true",
                        help="re-create data base")
    parser.add_argument("-l", "--load", action="store_true",
                        help="paste data from files to tables")
    parser.add_argument("--log", action="store", default="info",
                        help="enable logging")
    parser.add_argument("-r", "--report", action="store_true", default=False,
                        help="generates a report on fuel use")
    parser.add_argument("-s", "--startdate", action="store", default="1000-00-00",
                        help="set the start date for the report")
    parser.add_argument("-e", "--enddate", action="store", default="9999-00-00",
                        help="set the end date for the report")
    parser.add_argument("-f", "--filename", action="store", default="report",
                        help="set the name of the report file")
    parser.add_argument("-g", "--gasname", action="append", default=None,
                        help="set gas names for the report")
    parser.add_argument("-i", "--info", action="store_true", default=True,
                        help="display information about refueling in a report")
    parser.add_argument("--statistic", action="store_true", default=True,
                        help="display statistics about refueling in a report")
    args = parser.parse_args()

    logging.basicConfig(filename="logging.log",
                        level=args.log.upper(),
                        format="%(asctime)s %(name)s [%(levelname)s] : %(message)s")
    logger = logging.getLogger("MAIN")

    # Создаем базу данных заправок
    db = database.DataBase("data/database.db", args.recreate)

    if args.recreate:
        # Создаем таблицу запрвавок
        recreate(db, args)


    if args.load:
        # Вставляем данные из текстового файла в таблицу
        db.insert_list("fuel", "name, price", db.csv_to_list("data/fuel.csv"))

        # Получаем список значений из файла
        data = []
        for row in db.csv_to_list("data/trans.csv"):
            # Разбираем каждую строку
            # Получем id заправки из файла fuel.txt по названию заправки
            fuel_id = db.select("fuel", "id", "name = '" + row[2] + "'").fetchone()
            if fuel_id is None:
                logger.warning("Unknown gas name")
                continue
            data.append(tuple([row[0], row[1], fuel_id[0], row[3]]))
        db.insert_list("trans", "dtime, odometer, fuel_id, amount", data)

    db.commit()
    db.disconnect()

    if args.report is True:
        r = reporter.Reporter(args.startdate, args.enddate, args.gasname, args.filename)
        r.create_report(args.info, args.statistic)
        # reportgen.report(args.startdata, args.enddata, args.gasname, args.filename)


def recreate(database, args):
    database.create_table("fuel",
                          """
                          id INTEGER PRIMARY KEY,
                          name TEXT NOT NULL UNIQUE,
                          price INTEGER NOT NULL
                          """)

    # Создаем таблицу транзакций
    database.create_table("trans",
                          """
                          id INTEGER PRIMARY KEY,
                          dtime TEXT DEFAULT CURRENT_TIMESTAMP,
                          odometer INTEGER NOT NULL,
                          fuel_id INTEGER NOT NULL,
                          amount INTEGER NOT NULL,
                          FOREIGN KEY (fuel_id) REFERENCES fuel(id)
                          """)

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
    condition = "t.fuel_id = f.id"
    condition += " AND tt.id = (SELECT MAX(id) FROM trans WHERE id < t.id)"
    condition += " AND nt.id = (SELECT MIN(id) FROM trans WHERE id > t.id)"
    database.create_view("v_trans",
                         "trans t, trans tt, trans nt, fuel f",
                         """t.id, t.dtime,
                            nt.dtime as next_dtime,
                            tt.dtime as prev_dtime,
                            f.name,
                            t.odometer,
                            tt.odometer as last_odometer,
                            t.odometer - tt.odometer as mbs,
                            f.price,
                            t.amount,
                            t.amount * f.price / 100 as cost,
                            (t.odometer - tt.odometer) / t.amount as mpg,
                            t.amount * f.price / (t.odometer - tt.odometer) as mile_price
                         """, condition, re_create=True)


if __name__ == "__main__":
    main()