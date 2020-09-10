# from reportlab.pdfgen import canvas
import logging
import argparse

import database



# TODO: Изменить ключи для запуска report
# TODO: Добавить подстановку номера заправки в trans при вставке данных в эту таблицу



def main():
    parser = argparse.ArgumentParser(prog="fuel_stat",
                                     description="""Creating statistics 
                                                    based on generated tables""")
    parser.add_argument("-r", "--recreate", action="store_true",
                        help="re-create data base")
    parser.add_argument("-p", "--paste", action="store_true",
                        help="paste data from files to tables")
    parser.add_argument("--log", action="store", default="info",
                        help="enable logging")
    parser.add_argument("--report", action="store_true", default=None,
                        help="generates a report on fuel use")
    parser.add_argument("-s", action="store", default=None,
                        help="set the start date for the report")
    parser.add_argument("-e", action="store", default=None,
                        help="set the end date for the report")
    parser.add_argument("-f", action="store", default=None,
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

    if args.paste:
        # Вставляем данные из текстового файла в таблицу
        db.insert_list("fuel", "name, price", db.csv_to_list("data/fuel.csv"))
        # Вставляем данные из текстового файла в таблицу
        for data in db.csv_to_list("data/trans.csv"):
            # print(data[2])
            fuel_id = db.select("fuel", "id", "name = '" + data[2] + "'").fetchone()
            db.insert("trans", "dtime, odometer, fuel_id, amount",
                      data[0] + ", " + data[1] + ", " + str(fuel_id[0]) + ", " + data[3])


    if args.report is not None:
        # Объединяем данные из таблиц
        c = db.select("trans t, fuel f",
                      "t.dtime, f.name, f.price, t.odometer, t.amount, t.amount * f.price AS cost",
                      "t.fuel_id = f.id")
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