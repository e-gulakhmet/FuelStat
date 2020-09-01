# from reportlab.pdfgen import canvas
import logging

import database


# TODO: Дополнить документацию
# TODO: Добавить таблцу заправок
# TODO: Добавить таблицу транзакций
# TODO: Добавить параметры при запуске
# TODO: Добавить функцию считывания данных из файлов для создания базы данных
# TODO: Добавить логгирование



def main():
    # Инициализируем logging
    logging.basicConfig(filename="logging.log", level=logging.DEBUG, format="%(asctime)s %(name)s [%(levelname)s] : %(message)s")
    logger = logging.getLogger("MAIN")

    db = database.DataBase("fuel")

    db.create_table('''data INTEGER, name TEXT,
                 distance INTEGER, price REAL(20,1), quantity REAL(20,1),
                 total REAL(20,2)''')

    db.insert("730327,'Texaco',24370,59.9,13.5,8.00")

    print(db.select())



    # # Создаем pdf файл с таблицой
    # pdf_tabel = canvas.Canvas("fuel.pdf")
    # pdf_tabel.drawString(0, 0, str(dbc.fetchone()))
    # pdf_tabel.save()



if __name__ == "__main__":
    main()