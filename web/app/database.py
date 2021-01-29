import sqlite3
import logging
import os
import csv


# TODO: Добавить функцию отсуствия названия таблицы в select


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
        if re_create:
            self.logger.info("Deleting table...")
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
            self.logger.info("Connected to database file(" + database_file + ')')
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
    

    def create_view(self, view_name, table_name, data='*', condition=None, order_by=None, limit=None, re_create=False): # Создать таблицу
        """
        Создает вид таблицы(объект созданный на основе другой таблицы)
        исходя из указанной информации.

        Parameters
        -----------
        view_name : str
            Название которое нужно установить для вида таблица.
        table_name : str
            Название таблицы из которой, на основе которых будет
            создан вид таблицы
        data : str
            Данные, которые нужно вставить из таблицы
            Указываются через запятую.
            Например: father, mother, childcount
        condition : str
            Условие, по которому будут подбираться данные.
            Например: childcount > 1.
        order_by : str
            Элемент таблицы, по которому будет строится последовательность.
        limit : int
            Количество строк, которые будут в создаваемой view.
        re_create : bool
            Пересоздание таблицы
        """
        if self.connected is True:
            if re_create is True:
                self.logger.debug("Deleting view...")
                self.db.execute("DROP VIEW IF EXISTS " + view_name)
                self.logger.info("View was deleted")
            self.logger.debug("Creating view...")
            command = "CREATE VIEW " + view_name + " AS SELECT " + data + " FROM " + table_name
            if condition is not None:
                command += " WHERE " + condition
            try:
                self.logger.debug(command)
                self.db.execute(command)
                self.logger.info("View " + view_name + " was created")
            except sqlite3.Error as e:
                self.logger.warning(e)
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
                clms_command = ""
                if colums:
                    clms_command = "(" + colums + ")"
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
                clms_command = ""
                for r in range(0, len(data[0])):
                    if r < len(data[0]) - 1:
                        s += "?,"
                    else:
                        s += "?"
                if colums:
                    clms_command = "(" + colums + ")"
                command = "INSERT INTO " + table_name + clms_command + " VALUES (" + s + ")"

                self.logger.debug(command + " data: " + str(data))
                self.db.executemany(command, data)
                self.logger.info("Data was added to the table[" + table_name + "]")
            except sqlite3.Error as e:
                self.logger.warning(e)
        else:
            self.logger.warning("Not connected to database")


    def select(self, table_name, data='*', condition=None, order_by=None, limit=None): # Выделить данные из таблицы
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
        order_by : str
            Элемент таблицы, по которому будет строится последовательность.
        limit : int
            Количество строк в полученнос списке.
        
        Returns
        -------
        str
            Возвращает выделенные данные из таблицы
            в виде строки или нескольких строк
        """

        if self.connected:
            try:
                command = "SELECT " + data + " FROM " + table_name
                if condition is not None:
                    command += " WHERE " + condition
                if order_by is not None:
                    command += " ORDER BY " + order_by
                if limit is not None:
                    command += " LIMIT " + limit

                self.logger.debug(command)
                c = self.db.execute(command)
                self.logger.info("Data was selected from table[" + table_name + "]")
                return c
            except sqlite3.Error as e:
                self.logger.warning(e)
        else:
            self.logger.warning("Not connected to database")
    

    def update(self, table_name: str, data: str, condition: str): # Обновить данные в таблице
        """
        Обновляет данные в строках таблице, которые подхотят по условию.
        
        Parameters
        ----------
        table_name : str
            Название таблицы, в строках которой нужно обновить данные.
        data : str
            Столбцы и данные, которые будут подставлены в эти стролбцы.
            Пример: "name = 'John', age = 28
        condition : str
            Условие, по которому будут подбираться строки,
            которые нужно изменить.
        """

        if self.connected:
            try:
                command = ("UPDATE" + table_name + "SET " + data +
                           " WHERE " + condition)
                self.logger.debug(command)
                self.db.execute(command)
                self.logger.info(table_name + "colum's data was updated")
            except sqlite3.Error as e:
                self.logger.warning(e)
        else:
            self.logger.warning("Not connected to database")
        

    def delete(self, table_name: str, condition: str): # Удалить данные в таблице
        """
        Удаляет строки с данными из таблицы, которые подхотят по условию.
        
        Parameters
        ----------
        table_name : str
            Название таблицы, в строках которой нужно обновить данные.
        condition : str
            Условие, по которому будут подбираться строки,
            которые нужно удалить.
        """

        if self.connected:
            try:
                command = ("DELETE FROM" + table_name +
                           " WHERE " + condition)
                self.logger.debug(command)
                self.db.execute(command)
                self.logger.info("Rows from " + table_name + " were deleted")
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
        
    
    def csv_to_list(self, file_path):
        if self.connected:
            self.logger.debug("Converting csv file to list")
            data = []
            with open(file_path, newline="\n") as csv_file:
                for row in csv.reader(csv_file, delimiter=","):
                    lst = []
                    for t in row:
                        try:
                            lst.append(int(t))
                        except ValueError:
                            lst.append(t)
                            continue
                    data.append(tuple(lst))
            self.logger.info("File was converted")

            return data
