import sqlite3
import logging



# TODO: Добавить статус подключения к файлу
# TODO: Добавить удаления файла бызы данных
# TODO: Добавить точку входа для пересоздания файла



class DataBase():
    """
    Класс создания и настройки базы данных.

    """


    def __init__(self, database_file):
        """
        Инициализация базы данных.
        Подлкючаемся к базе данных.

        Parameters
        ----------
        database_file : str
            Путь к файлу базы данных

        """

        self.logger = logging.getLogger("DATABASE")

        # Подключаемся к базе данных
        try:
            self.logger.debug("Connecting to database...")
            self.db = sqlite3.connect(database_file)
            self.logger.info("Connected to database file(" + database_file)
        except sqlite3.Error as e:
            self.logger.error(e)

    def create_table(self, table_name, colums_name, re_create=False): # Создать таблицу
        """
        Создает таблицу исходя из указанной информации.

        Parameters:
        -----------
        table_name : str
            Название которое нужно установить для таблицы.
        colums_name : str
            Назваения столбцов таблицы.
            Указываются через запятую.
            Например: father TEXT, mother TEXT, childcount INT
        re_create : bool
            Если данный флаг активен, база данных пересоздатся.
            В итоге будет пустая база данных, без таблиц.
        """

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
        """
        Вставляет данные в созданную таблицу.

        Parameters
        ----------
        table_name : str
            Имя таблицы в которую нужно вставить данные.
        colums : str
            Имена столбцов в таблицу,
            в которые нужно будет вставить данные.
            Записываются через запятую.
            Например: father, mother, childcount.
            Если ничего не указывать, то данные
            присвоятся всем столбцам, взависимости от 
            последовательности переданных данных.
        data : str, int
            Данные, которые вставляются в таблицу.
            Записываются в порядке столбцов в таблице,
            либо в порядке столбцов, которые мы указали.
            Указываются черех запятую.
            Например, если столбцы равны:
                father, mother, child count
            То данные должны быть переданны в таком виде:
                Jon, Marry, 8
        """
        
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
