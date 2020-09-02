import sqlite3
import logging



class DataBase():
    def __init__(self, database_name):
        self.database_name = database_name
        self.logger = logging.getLogger("DATABASE")

        # Подключаемся к базе данных
        try:
            self.logger.debug("Connecting to database...")
            self.db = sqlite3.connect("data/" + database_name + ".db")
            self.logger.info("Connected to database file(" + self.database_name + '.db)')
        except sqlite3.Error as e:
            self.logger.error(e)

    def create_table(self, colums_name): # Создать таблицу
        self.logger.debug("Creating table...")
        try:
            self.db.execute("CREATE TABLE IF NOT EXISTS " + self.database_name + " (" + colums_name + ")")
            self.logger.info("Table " + self.database_name + "was created")
        except sqlite3.Error as e:
            self.logger.warning(e)
    

    def insert(self, colums=None, data=None): # Вставить значения в таблицу
        try:
            if colums is None:
                self.logger.debug("Inserting listdata[" + data + "]")
                self.db.execute("INSERT INTO " + self.database_name + " VALUES (" + data + ")")
            else:
                self.logger.debug("Inserting listdata[" + data + "] into colums[" + colums + ']')
                self.db.execute("INSERT INTO " + self.database_name + "(" + colums + ") VALUES (" + data + ")")
            self.logger.info("Data was added to the table")
        except sqlite3.Error as e:
            self.logger.warning(e)
    
    def insert_list(self, colums=None, data=None): # Вставить списки со значениями в таблицу
        try:
            s = ""
            for r in range(0, len(data[0])):
                if r < len(data[0]) - 1:
                    s += "?,"
                else:
                    s += "?"
            if colums is None:
                self.logger.debug("Inserting listdata[" + str(data) + "]")
                self.db.execute("INSERT INTO " + self.database_name + " VALUES (" + s + ')', data)
            else:
                self.logger.debug("Inserting listdata[" + str(data) + "] into colums[" + colums + ']')
                self.db.executemany("INSERT INTO " + self.database_name + "(" + colums + ") VALUES (" + s + ")", data)
            self.logger.info("Data was added to the table")
        except sqlite3.Error as e:
            self.logger.warning(e)


    def select(self, data='*', condition=None): # Выделить данные из таблицы
        try:
            if condition is None:
                self.logger.debug("Selecting data[" + data + "]")
                c = self.db.execute("SELECT " + data + " FROM " + self.database_name)
            else:
                self.logger.debug("Selecting data[" + data + "] with condition[" + condition + "]from the table...")                
                c = self.db.execute("SELECT " + data + " FROM " + self.database_name + " WHERE " + condition)
            self.logger.info("Data was selected from table")
            return c
        except sqlite3.Error as e:
            self.logger.warning(e)