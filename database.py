import sqlite3
import logging
import os
import csv


# TODO: Добавить точку входа для пересоздания файла



class DataBase():
    """
    Класс создания и настройки базы данных.

    """


    def __init__(self, database_file, re_create=False):
        """
        Инициализация базы данных.
        Подлкючаемся к базе данных.

        Parameters
        ----------
        database_file : str
            Путь к файлу базы данных
        re_create : bool
            Если данный флаг активен, база данных пересоздатся.
            В итоге будет пустая база данных, без таблиц.

        """

        self.logger = logging.getLogger("DATABASE")

        self.connected = False

        # Удаляем файл базу данных
        self.logger.info("Deleting table...")
        if re_create:
            try:
                os.remove(database_file)
                self.logger.info("Database was deleted")
            except FileNotFoundError:
                self.logger.info("Database not found")


        # Подключаемся к базе данных
        self.logger.debug("Connecting to database...")
        try:
            self.db = sqlite3.connect(database_file)
            self.connected = True
            self.logger.info("Connected to database file(" + database_file)
        except sqlite3.Error as e:
            self.logger.error(e)

    def create_table(self, table_name, colums_name): # Создать таблицу
        """
        Создает таблицу исходя из указанной информации.
        Если при вызове передан txt file, то программа
        заполнит таблицу данными этого файла.

        Parameters
        -----------
        table_name : str
            Название которое нужно установить для таблицы.
        colums_name : str
            Назваения столбцов таблицы.
            Указываются через запятую.
            Например: father TEXT, mother TEXT, childcount INT
        txt_file_path : str
            Если флаг активен, то данные из этого файла будут
            сразу загружены в таблицу
        """
        if self.connected is True:
            self.logger.debug("Creating table...")
            try:
                self.db.execute("CREATE TABLE IF NOT EXISTS " + table_name + " (" + colums_name + ")")
                self.logger.info("Table " + table_name + "was created")
            except sqlite3.Error as e:
                self.logger.warning(e)
        else:
            self.logger.warning("Not connected to database")
    

    def insert_file(self, table_name, colums=None, file_path=None):
        """
        Вставляет данные из файла в созданную таблицу

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
        file_path : str
            Путь к файлу, в котором содержаться данные
            для таблицы
        """
        if self.connected:
            data = []
            with open(file_path, newline="\n") as csv_file:
                for row in csv.reader(csv_file, delimiter=","):
                    lst = []
                    for t in row:
                        try:
                            lst.append(t)
                        except ValueError:
                            lst.append(int(t))
                            continue
                    data.append(tuple(lst))
            self.logger.debug("File was opened")
            print(data)
            
            self.insert_list(table_name, colums, data)
        else:
            self.logger.warning("Not connected to database")


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
        if self.connected:
            try:
                command = ""
                if colums is None:
                    command = "INSERT INTO " + table_name + " VALUES (" + data + ")"
                else:
                    command = "INSERT INTO " + table_name + "(" + colums + ") VALUES (" + data + ")"
                self.logger.debug(command)
                self.db.execute(command)
                self.logger.info("Data was added to the table[" + table_name + "]")
            except sqlite3.Error as e:
                self.logger.warning(e)
        else:
            self.logger.warning("Not connected to database")

    
    def insert_list(self, table_name, colums=None, data=None): # Вставить списки со значениями в таблицу
        """
        Вставляет список с данными в созданную таблицу.
        Нужно для того, чтобы вствить сразу несолько строк
        данных при помощи одной команды.

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
        data : list
            Список кортежей, в которых находтся данные вставляемые в таблицу.
            Записываются в порядке столбцов в таблице,
            либо в порядке столбцов, которые мы указали.
            Имеют вид l = [('A', 1), (B, 6)]
            Например, если столбцы равны:
                father, mother, child count
            при этом мы хотим сразу заполнить сразу несколько строк
            То данные должны быть переданны в таком виде:
                [("Jon", "Marry", 8), ("Alex", "Lora", 1)]
        """
        if self.connected:
            try:
                s = ""
                for r in range(0, len(data[0])):
                    if r < len(data[0]) - 1:
                        s += "?,"
                    else:
                        s += "?"
                command = ""
                if colums is None:
                    command = "INSERT INTO " + table_name + " VALUES (" + s + ')'
                else:
                    command = "INSERT INTO " + table_name + "(" + colums + ") VALUES (" + s + ")"
                self.logger.debug(command)
                self.db.executemany(command, data)
                self.logger.info("Data was added to the table[" + table_name + "]")
            except sqlite3.Error as e:
                self.logger.warning(e)
        else:
            self.logger.warning("Not connected to database")


    def select(self, table_name, data='*', condition=None): # Выделить данные из таблицы
        """
        Выделяет данные из таблицы и возвращает их.

        Parameters
        ----------
        table_name : str
            Название таблицы, из которуй нужно
            достать данные.
        data : str
            Названия столбцов, в которых лежат нужные данные.
            Записываются через запятую.
            Например: father, mother, childcount.
            Если данные параметр не указан, то будут получены
            данные из всех столбов данной таблицы.
        condition : str
            Условие, по которому будут подбираться данные.
            Например: childcount > 1.
        
        Returns
        -------
        str
            Возвращает выделенные данные из таблицы
            в виде строки или нескольких строк

        
        Examples
        --------
            >>> c = select("table", "father", "childcount > 1")
            >>> for row in c:
            >>>     print(row)
            "Jon"
            "Alex"
        """
        if self.connected:
            try:
                if condition is None:
                    command = "SELECT " + data + " FROM " + table_name
                else:
                    command = "SELECT " + data + " FROM " + table_name + " WHERE " + condition
                self.logger.debug(command)
                c = self.db.execute(command)
                self.logger.info("Data was selected from table[" + table_name + "]")
                return c
            except sqlite3.Error as e:
                self.logger.warning(e)
        else:
            self.logger.warning("Not connected to database")
    
    def commit(self):
        if self.connected:
            self.logger.debug("Commiting database")
            try:
                self.db.commit()
                self.logger.info("Database was commited")
            except sqlite3.Error as e:
                self.logger.warning(e)
        else:
            self.logger.warning("Not connected to database")

    def disconnect(self):
        if self.connected:
            self.logger.debug("Disconnecting from the database")
            try:
                self.db.close()
                self.connected = False
                self.logger.info("Disconnected from the database")
            except sqlite3.Error as e:
                self.logger.warning(e)
        else:
            self.logger.warning("Not connected to database")       
