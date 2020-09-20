# from reportlab.pdfgen import canvas
import logging
import argparse

import database



# TODO: Собрать генератор исходных значений
# TODO: Добавить проверку таблиц в базе данных на последовательность данных пробега
# TODO: Добавить проверку даты транзакции



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
    parser.add_argument("-r", "--report", action="store_true", default=None,
                        help="generates a report on fuel use")
    parser.add_argument("-s", "--startdata", action="store", default=None,
                        help="set the start date for the report")
    parser.add_argument("-e", "--enddata", action="store", default=None,
                        help="set the end date for the report")
    parser.add_argument("-f", "--filename", action="store", default="report",
                        help="set the name of the report file")
    parser.add_argument("-g", "--gasname", action="append", default=None,
                        help="set the name of the report file")
    args = parser.parse_args()

    logging.basicConfig(filename="logging.log",
                        level=args.log.upper(),
                        format="%(asctime)s %(name)s [%(levelname)s] : %(message)s")
    logger = logging.getLogger("MAIN")

    # Создаем базу данных заправок
    db = database.DataBase("data/database.db", args.recreate)

    if args.recreate:
        # Создаем таблицу запрвавок
        db.create_table("fuel",
                        """id INTEGER PRIMARY KEY,
                           name TEXT NOT NULL UNIQUE,
                           price INTEGER NOT NULL""")

        # Создаем таблицу транзакций
        db.create_table("trans",
                        """id INTEGER PRIMARY KEY,
                           dtime TEXT DEFAULT CURRENT_TIMESTAMP,
                           odometer INTEGER NOT NULL,
                           fuel_id INTEGER NOT NULL,
                           amount INTEGER NOT NULL,
                           FOREIGN KEY (fuel_id) REFERENCES fuel(id)""")

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


    if args.report is not None:
        print("Report parameters: " + str(args.startdata) + " " + str(args.enddata) +
              " " + str(args.filename) + " " + str(args.gasname))

        # Объединяем данные из таблиц
        c = db.select("trans t, fuel f",
                      "t.dtime, f.name, f.price, t.odometer, t.amount, t.amount * f.price / 100 AS cost",
                      "t.fuel_id = f.id" +
                      " AND DATE(t.dtime) >= '" + str(args.startdata) + "'" +
                      " AND t.dtime <= '" + str(args.enddata) + "'" +
                      " AND f.name in " + str(tuple(args.gasname)) +
                      " ORDER BY t.dtime")

        for row in c:
            print(row)
        print("\n")


    for row in db.select("fuel"):
        print(row)
    print("\n")

    for row in db.select("trans"):
        print(row)
    print("\n")


    db.commit()
    db.disconnect()

    # # Создаем pdf файл с таблицой
    # pdf_tabel = canvas.Canvas("db.pdf")
    # pdf_tabel.drawString(0, 0, str(dbc.fetchone()))
    # pdf_tabel.save()


if __name__ == "__main__":
    main()