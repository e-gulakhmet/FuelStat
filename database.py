import sqlite3
import logging



class DataBase():
    def __init__(self, database_name):
        self.database_name = database_name
        self.logger = logging.getLogger("DATABASE")

        # Подключаемся к базе данных
        self.logger.info("Connecting to database...")
        try:
            self.db = sqlite3.connect("data/" + database_name + ".db")
            self.logger.info("Connected to database file")
        except sqlite3.Error as e:
            self.logger.error(e)

        self.logger.info("Creating cursor...")
        # Создаем курсор дл управления базой данных
        try:
            self.dbc = self.db.cursor()
            self.logger.info("DataBase cursor was created")
        except sqlite3.Error as e:
            self.logger.error(e)


    def create_table(self, colums_name): # Создать таблицу
        self.logger.info("Creating table...")
        try:
            self.dbc.execute("CREATE TABLE " + self.database_name + " (" + colums_name + ")")
            self.logger.info("Table was created")
        except sqlite3.Error as e:
            self.logger.warning(e)
    

    def insert(self, data): # Вставить значения в таблицу
        self.logger.info("Inserting data into the table...")
        try:
            self.dbc.execute("INSERT INTO " + self.database_name + " VALUES (" + data + ")")
            self.logger.info("Data has been added to the table")
        except sqlite3.Error as e:
            self.logger.warning(e)


    def select(self, data='*', condition=None): # Выделить данные из таблицы
        self.logger.info("Selecting data from the table...")
        try:
            if condition is None:
                self.dbc.execute("SELECT " + data + " FROM " + self.database_name)
                self.logger.info("Data was selected from table")
            else:
                self.dbc.execute("SELECT " + data + " FROM " + self.database_name + " WHERE " + condition)
                self.logger.info("Data was selected from table with condition")
            return self.dbc.fetchone()
        except sqlite3.Error as e:
            self.logger.warning(e)