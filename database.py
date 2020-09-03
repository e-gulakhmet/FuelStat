import sqlite3
import logging



class DataBase():
    def __init__(self, database_file):
        self.logger = logging.getLogger("DATABASE")

        # Подключаемся к базе данных
        try:
            self.logger.debug("Connecting to database...")
            self.db = sqlite3.connect(database_file)
            self.logger.info("Connected to database file(" + database_file)
        except sqlite3.Error as e:
            self.logger.error(e)

    def create_table(self, table_name, colums_name, re_create=False): # Создать таблицу
        if re_create:
            self.logger.debug("Deleting table...")
            try:
                self.db.execute("DROP TABLE IF EXISTS " + table_name)
                self.logger.info("Table was droped")
            except sqlite3.Error as e:
                self.logger.warning(e)
        self.logger.debug("Creating table...")
        try:
            self.db.execute("CREATE TABLE IF NOT EXISTS " + table_name + " (" + colums_name + ")")
            self.logger.info("Table " + table_name + "was created")
        except sqlite3.Error as e:
            self.logger.warning(e)
    

    def insert(self, table_name, colums=None, data=None): # Вставить значения в таблицу
        try:
            if colums is None:
                self.logger.debug("Inserting into [" + table_name + "] listdata[" + data + "]")
                self.db.execute("INSERT INTO " + table_name + " VALUES (" + data + ")")
            else:
                self.logger.debug("Inserting listdata[" + data + "] into colums[" + colums + ']')
                self.db.execute("INSERT INTO " + table_name + "(" + colums + ") VALUES (" + data + ")")
            self.logger.info("Data was added to the table[" + table_name + "]")
        except sqlite3.Error as e:
            self.logger.warning(e)
    
    def insert_list(self, table_name, colums=None, data=None): # Вставить списки со значениями в таблицу
        try:
            s = ""
            for r in range(0, len(data[0])):
                if r < len(data[0]) - 1:
                    s += "?,"
                else:
                    s += "?"
            if colums is None:
                self.logger.debug("Inserting into [" + table_name + "] listdata[" + str(data) + "]")
                self.db.execute("INSERT INTO " + table_name + " VALUES (" + s + ')', data)
            else:
                self.logger.debug("Inserting into [" + table_name + "] listdata [" + str(data) + "] into colums[" + colums + ']')
                self.db.executemany("INSERT INTO " + table_name + "(" + colums + ") VALUES (" + s + ")", data)
            self.logger.info("Data was added to the table[" + table_name + "]")
        except sqlite3.Error as e:
            self.logger.warning(e)


    def select(self, table_name, data='*', condition=None): # Выделить данные из таблицы
        try:
            if condition is None:
                self.logger.debug("Selecting data[" + data + "] from [" + table_name + "]")
                c = self.db.execute("SELECT " + data + " FROM " + table_name)
            else:
                self.logger.debug("Selecting data[" + data + "] with condition[" + condition + "]from the table...")                
                c = self.db.execute("SELECT " + data + " FROM " + table_name + " WHERE " + condition)
            self.logger.info("Data was selected from table[" + table_name + "]")
            return c
        except sqlite3.Error as e:
            self.logger.warning(e)
    
    def commit(self):
        self.logger.debug("Commiting database")
        try:
            self.db.commit()
            self.logger.info("Database was commited")
        except sqlite3.Error as e:
            self.logger.warning(e)

    def disconnect(self):
        self.logger.debug("Disconnecting from the database")
        try:
            self.db.close()
            self.logger.info("Disconnected from the database")
        except sqlite3.Error as e:
            self.logger.warning(e)
