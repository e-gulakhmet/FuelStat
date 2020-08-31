import sqlite3



def main():
    # Подключаемся к базе данных
    db = sqlite3.connect('fuel.db')
    # Создаем курсор дл управления базой данных
    dbc = db.cursor()

    # Создаем таблицу
    dbc.execute('''CREATE TABLE IF NOT EXISTS fuel (data INTEGER, name TEXT,
                  distance INTEGER, price REAL(20,1), quantity REAL(20,1),
                  total REAL(20,2))''')
    # Вставляем значения в таблицу
    dbc.execute("INSERT INTO fuel VALUES (730327,'Texaco',24370,59.9,13.5,8.00)")

    dbc.execute("SELECT * FROM fuel WHERE data == 730327")
    print(dbc.fetchone())

    # Сохраняем изменения
    db.commit()

    # Отключаемся от базы данных
    db.close()




if __name__ == "__main__":
    main()