import sqlite3
import logging



class DataBase():
    def __init__(self, database_name):
        self.database_name = database_name
        self.logger = logging.getLogger("DATABASE")

        # Подключаемся к базе данных
        try:
            self.logger.info("Connecting to database...")
            self.db = sqlite3.connect("data/" + database_name + ".db")
            self.logger.info("Connected to database file")
            self.logger.info("Creating cursor...")
            self.dbc = self.db.cursor()
            self.logger.info("DataBase cursor was created")
        except sqlite3.Error as e:
            self.logger.error(e)

        # self.logger.info("Creating cursor...")
        # # Создаем курсор дл управления базой данных
        # try:

        # except sqlite3.Error as e:
        #     self.logger.error(e)


    def create_table(self, colums_name): # Создать таблицу
        self.logger.info("Creating table...")
        try:
            self.dbc.execute("CREATE TABLE IF NOT EXISTS " + self.database_name + " (" + colums_name + ")")
            self.logger.info("Table was created")
        except sqlite3.Error as e:
            self.logger.warning(e)
    

    def insert(self, colums=None, data=None): # Вставить значения в таблицу
        self.logger.info("Inserting data into the table...")
        try:
            if colums is None:
                self.dbc.execute("INSERT INTO " + self.database_name + " VALUES (" + data + ")")
            else:
                self.dbc.execute("INSERT INTO " + self.database_name + "(" + colums + ") VALUES (" + data + ")")
            self.logger.info("Data was added to the table")
        except sqlite3.Error as e:
            self.logger.warning(e)
    
    def insert_list(self, colums=None, data=None): # Вставить списки со значениями в таблицу
        self.logger.info("Inserting listdata into the table...")
        # # try:
        # #     d = ""
        # #     i = 0
        # #     for s in data:
        # #         r = ""
        # #         g = 0
        # #         for t in s:
        # #             if g == 0:
        # #                 r = "( " + t
        # #             else:
        # #                 r += ", " + t
        # #             g += 1
        # #         if i == 0:
        # #             d = r + ")"
        # #         else:
        # #             d += ", " + t + ") "
        # #         i +=1
            
        #     print(d)
        try:
            s = ""
            for r in range(0, len(data[0])):
                if r < len(data[0]) - 1:
                    s += "?,"
                else:
                    s += "?"
            # for r in range(0, len(data)):
            #     if r < len(data) - 1:
            #         s += "?," 
            #     else:
            #         s += "?"
            print(s)
            
            if colums is None:
                self.dbc.execute("INSERT INTO " + self.database_name + " VALUES (" + s + ')', data)
            else:
                self.dbc.execute("INSERT INTO " + self.database_name + '(' + colums + ") VALUES (" + s + ')', data)
            self.logger.info("Data was added to the table")
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