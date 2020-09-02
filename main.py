# from reportlab.pdfgen import canvas
import logging
import argparse

import database


# TODO: Дополнить документацию
# TODO: Добавить параметры при запуске
# TODO: Сделать объединение баз данных



def main():
    parser = argparse.ArgumentParser(prog="fuel_stat",
                                     description="""Creating statistics 
                                                    based on generated tables""")

    parser.add_argument("--recreate", action="store_true",
                        help="re-create all data base")
    args = parser.parse_args()


    logging.basicConfig(filename="logging.log",
                        level=logging.DEBUG,
                        format="%(asctime)s %(name)s [%(levelname)s] : %(message)s")
    logger = logging.getLogger("MAIN")

    # Создаем базу данных заправок
    fuel = database.DataBase("fuel")

    fuel.create_table('''id INTEGER PRIMARY KEY,
                         name TEXT NOT NULL,
                         price INTEGER NOT NULL''', args.recreate)

    # for s in fuels:
    #     gas = s.split(", ")
    #     fuel.insert("name, price", "'" + gas[0] + "', " + gas[1])

    fuel.insert_list("name, price", txt_to_list("data/fuel.txt"))

    for row in fuel.select():
        print(row)
    print("\n")


    # Создаем базу данных транзакций
    trans = database.DataBase("trans")
    trans.create_table("""id INTEGER PRIMARY KEY,
                          dtime TEXT DEFAULT CURRENT_TIMESTAMP,
                          odometer TEXT NOT NULL,
                          fuel_id TEXT NOT NULL,
                          amount TEXT NOT NULL,
                          FOREIGN KEY (fuel_id) REFERENCES fuel(id)""")
    trans.insert_list("dtime, odometer, fuel_id, amount", txt_to_list("data/trans.txt"))

    for row in trans.select():
        print(row)


    # Объединяем базы данных
    general = database.DataBase("general"):
    general.create_table("""dtime, name, odometr,  """)


    # # Создаем pdf файл с таблицой
    # pdf_tabel = canvas.Canvas("fuel.pdf")
    # pdf_tabel.drawString(0, 0, str(dbc.fetchone()))
    # pdf_tabel.save()



def txt_to_list(file_path): # Открыть и преобразовать текстовый файл
    # На вход получаем путь к текстовому полю
    # На выходе получаем список со строками
    file_txt = open(file_path, 'r').read()
    lines = file_txt.split("\n")
    # for s in fuels:
    #     gas = s.split(", ")
    #     fuel.insert("name, price", "'" + gas[0] + "', " + gas[1])

    data = []
    for line in lines:
        data.append(tuple(line.split(", ")))
    return data




if __name__ == "__main__":
    main()