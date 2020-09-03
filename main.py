# from reportlab.pdfgen import canvas
import logging
import argparse

import database


# TODO: Дополнить документацию
# TODO: Добавить параметры при запуске
# TODO: Задокументировать txt файлы



def main():
    parser = argparse.ArgumentParser(prog="fuel_stat",
                                     description="""Creating statistics 
                                                    based on generated tables""")

    parser.add_argument("--recreate", action="store_true",
                        help="re-create all data base")
    args = parser.parse_args()

# TODO: Переконвертировать данные из TEXT в INTEGER
    logging.basicConfig(filename="logging.log",
                        level=logging.DEBUG,
                        format="%(asctime)s %(name)s [%(levelname)s] : %(message)s")
    logger = logging.getLogger("MAIN")

    # Создаем базу данных заправок
    db = database.DataBase("data/database.db")

    db.create_table("fuel",
                    '''id INTEGER PRIMARY KEY,
                       name TEXT NOT NULL,
                       price INTEGER NOT NULL''',
                    args.recreate)

    # for s in dbs:
    #     gas = s.split(", ")
    #     db.insert("name, price", "'" + gas[0] + "', " + gas[1])

    db.insert_list("fuel", "name, price", txt_to_list("data/fuel.txt"))

    for row in db.select("fuel"):
        print(row)
    print("\n")


    db.create_table("trans",
                    """id INTEGER PRIMARY KEY,
                       dtime TEXT DEFAULT CURRENT_TIMESTAMP,
                       odometer INTEGER NOT NULL,
                       fuel_id INTEGER NOT NULL,
                       amount INTEGER NOT NULL,
                       FOREIGN KEY (fuel_id) REFERENCES fuel(id)""",
                    args.recreate)

    db.insert_list("trans", "dtime, odometer, fuel_id, amount", txt_to_list("data/trans.txt"))

    for row in db.select("trans"):
        print(row)
    print("\n")

    # Объединяем таблицы
    c = db.select("trans t, fuel f",
                  "t.dtime, f.name, f.price, t.odometer, t.amount, t.amount * f.price AS cost",
                  "t.fuel_id = f.id")

    for row in c:
        print(row)
    print("\n")

    # # Создаем pdf файл с таблицой
    # pdf_tabel = canvas.Canvas("db.pdf")
    # pdf_tabel.drawString(0, 0, str(dbc.fetchone()))
    # pdf_tabel.save()



def txt_to_list(file_path): # Открыть и преобразовать текстовый файл
    # На вход получаем путь к текстовому полю
    # На выходе получаем список со строками
    file_txt = open(file_path, 'r').read()
    lines = file_txt.split("\n")

    data = []
    for line in lines:
        lst = []
        for t in line.split(", "):
            try:
                lst.append(int(t))
            except ValueError:
                lst.append(t)
                continue
        data.append(tuple(lst))
    return data




if __name__ == "__main__":
    main()