import logging
import database
# from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer, Flowable
from reportlab.lib.styles import getSampleStyleSheet


# TODO: Сделать документ в альбомном формате
# TODO: Выровнять поля(текст влево, цифры вправо)
# TODO: Добавить поля(дюим, 25мм)
# TODO: Изменить таблицу статистики(строки перенести в столбцы)



class MyLine(Flowable):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
    
    def draw(self):
        self.canv.line(0, self.height, self.width, self.height)



class Reporter():
    """
    Класс создания отчета
    """

    def __init__(self, start_date="1000-00-00", end_date="9999-00-00", gas_name=None,
                 file_name="report"):
        """
        Инициализация класса.
        Создаем документ, который затем будет содержать
        и выводить свои элементы.

        Parameters
        ----------
        start_data : str
            Дата, с которой будет начинаться отчет.
        end_data : str
            Конечная дата отчета.
        gas_name : str
            Названия заправок по которым будет строиться отчет.
        file_name : str
            Название файла отчета.
        """

        self.start_date = start_date
        self.end_date = end_date
        self.gas_name = gas_name
        self.file_name = file_name

        self.logger = logging.getLogger("REPORTER")  
        self.logger.debug("Report parameters: start_date[" + str(self.start_date) + ']' +
                          ", end_date[" + str(self.end_date) + ']' +
                          ", gas_names[" + str(self.gas_name) + ']' +
                          ", file_name[" + str(self.file_name) + ']')
    
        self.db = database.DataBase("data/database.db")
    
        # Cоздаем документ, в котором будут содержать полученные данные
        self.logger.debug("Creating DocTemplate")
        self.doc = SimpleDocTemplate("data/" + file_name + ".pdf",
                                     pagesize=A4,
                                     topMargin=5 * mm,
                                     bottomMargin=5 * mm,
                                     leftMargin=10 * mm,
                                     rightMargin=10 * mm,
                                     showBoundary=0)
        self.logger.info("DocTemplate was created")

        self.elements = [] # Список, который будет содержать все элементы документа

        # Создаем нужные нам стили
        styles = getSampleStyleSheet()
        self.s_header_1 = styles["Heading1"]
        self.s_header_1.alignment = TA_CENTER
        self.s_param = styles["Normal"]
        self.s_param.fontSize = 12
        self.s_param.spaceAfter = 10
        self.s_header_2 = styles["Heading2"]
        self.s_header_2.alignment = TA_CENTER
        self.s_text = styles["Normal"]
        self.s_text.fontSize = 14
        self.s_table = [("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                        ('ALIGN', (0, 0), (-1, -1), "CENTER"),
                        ('VALIGN', (0, 0), (-1, -1), "MIDDLE")]


        # Название документа
        self.elements.append(Paragraph("FuelStatReport", self.s_header_1))
        self.elements.append(Spacer(0, 20))

        # Информация о параметрах отчета
        param_info = "Start Date: " + self.start_date
        param_info += "&nbsp;&nbsp;&nbsp;&nbsp; End Date: " + self.end_date
        gs = ""
        # Создаем строку с названями заправки
        if self.gas_name is None:
            gs = "All"
        else:
            gs = str(self.gas_name[0])
            for n in self.gas_name:
                gs += ", " + str(n)
        param_info += "&nbsp;&nbsp;&nbsp;&nbsp; Gas Stations: " + gs
        self.elements.append(Paragraph(param_info, self.s_param))

        # Рисуем линию после параметров отчета
        self.elements.append(MyLine(self.doc.width, 0))
        self.elements.append(Spacer(0, 20))

        self.condition = "dtime >= '" + str(self.start_date) + "'"
        self.condition += " AND dtime <= '" + str(self.end_date) + "'" 
        if self.gas_name is not None:
            self.condition += " AND name in " + str(tuple(self.gas_name))


    
    def create_report(self, main_info=True, statistic=True):
        if main_info is True:
            self.elements.extend(self.gen_main_info())
        if statistic is True:
            self.elements.extend(self.gen_stat())
        self.doc.build(self.elements)



    def gen_main_info(self):
        """
        Генерирует элементы для основоного отчета,
        в котором будет данные о заправках. \n
        Не формирует статистистическую информацию! \n
        Данные:
        - Дата заправки;
        - Название заправки;
        - Расстояние пройденное до этой заправки(мили);
        - Цена одного галлона(центы);
        - Расстояние, пройденное после предыдущей заправки(мили);
        - Количество галлонов;
        - Общая стоимость заправки(доллары);
        - Расстояние пройденно на одном галлоне(мили);
        - Цена одной мили(доллары);
        - Цена одного дня(доллары);

        Returns
        -------
        list:
            Список элементов основного отчета
        """

        elements = []

        # Получаем данные из базы данных
        # Условия получения информации из вьюшки для цены дня:
        # Если дата текущей заправки равна дате предыдущей заправки,
        # то прибавляем ее цену к сумме.
        # Если даты разные, то сохраняем сумму в предыдущую заправку, затем
        # сумму приравниваем к цене текущей запраки.
        table_data = self.table_data_to_list(
            self.db.select("v_trans vv", 
                           """dtime,
                           name,
                           odometer,
                           mbs,
                           price,
                           amount,
                           cost,
                           mpg,
                           mile_price,
                           CASE next_dtime = dtime
                              WHEN FALSE
                                THEN (
                                      SELECT SUM(v.cost) 
                                      FROM v_trans v 
                                      WHERE v.dtime = vv.dtime AND
                           """ + self.condition +
                           """
                                      GROUP BY v.dtime
                                     )
                           END
                            """, condition=self.condition, order_by="dtime"))

        table_data.insert(0,
                          ["DATE", "GAS \n STATION", "ODOMETER",
                           "MILIAGE \n BEETWEEN",
                           "GALLON \n PRICE",
                           "GALLONS", "COST", "MPG", 
                           "MILE \n PRICE", "DAY \n PRICE"])


        # После получения данных из вьюшки нужно создать список,
        # в котором будут хранится строки,
        # которые нужно объединить объединить в таблице.
        # Элемент списка будет выглядить вот так: [s_cell, e_cell]
        merge_rows = []
        merging = False
        # В списке, который мы получили от базы данны, проверяем:
        self.logger.debug("Creating merging rows list for document's table")
        for i in range(1, len(table_data)):
            # Если ячейка цены дня пустая и флажок объединения не активен:
            if table_data[i][9] is None and merging is False:
                # Записываем текущую строку, как начальную для объединения и
                # активируем флажок объединения.
                merge_rows.append([i, ])
                merging = True
            # Если ячейка цены дня не пустая и флажок объединения активен,
            elif table_data[i][9] is not None and merging is True:
                # то указываем текущую ячейку, как конечную для объединения и
                # выключаем флажок объединения.
                table_data[merge_rows[len(merge_rows) - 1][0]][9] = table_data[i][9]
                merge_rows[len(merge_rows) - 1].append(i)
                merging = False
        self.logger.debug("Merging rows is " + str(merge_rows))
        self.logger.info("Merging rows list was created")


        # Создаем таблицу
        self.logger.debug("Creating document's main table")
        table = Table(table_data, repeatRows=True)
        table_style = self.s_table
        for row in merge_rows:
            table_style.append(("SPAN", (9, row[0]), (9, row[1])))
        table.setStyle(TableStyle(table_style))
        self.logger.info("Document's main table was created")
        elements.append(table)
        elements.append(Spacer(0, 20))

        return elements



    def gen_stat(self):
        """
        Генерирует элементы для статистике в отчете. \n
        Данные таблицы с краткой статистикой:
        - Общее пройденное расстояние(мили).
        - Среднее расстояние между заправками(мили).
        - Средняя цена галлона(центы).
        - Среднее количество галлонов.
        - Средняя цена одной заправки(доллары).
        - Общая цена всех заправок(доллары).
        - Средний пробег на одном галлоне(мили).
        - Средняя цена одной мили(доллары).
        - Средний расход топлива(галлоны).

        Основная статистика:
        - Самая часто посещаемая вами заправка.
        - Самая выгодная заправка и информация о ней.
        - Количество долларов, которые можно было сэкономить,
          если заправляться только на самой выгодной заправке.

        Returns
        -------
        list
            Элементы краткой статистики
        """

        elements = []

        # Данные по статистике
        elements.append(Paragraph("Statistics", self.s_header_1))
        elements.append(Spacer(0, 5))

        table_data = self.table_data_to_list(
            self.db.select("v_trans",
                           """
                           MAX(odometer) - MIN(odometer),
                           AVG(mbs),
                           AVG(price),
                           AVG(amount),
                           AVG(cost),
                           SUM(cost),
                           AVG(mpg),
                           AVG(mile_price),
                           SUM(amount) / (MAX(odometer) - MIN(odometer)) * 60
                           """, condition=self.condition))

        table_data.insert(0, 
                          ["TOTAL \n DISTANCE",
                           "AVERAGE \n MILIAGE \n BEETWEEN",
                           "AVERAGE \n GALLON \n PRICE",
                           "AVERAGE \n GALLONS",
                           "AVERAGE \n COST", "TOTAL \n COST",
                           "AVERAGE \n MPG", "AVERAGE \n MILE \n PRICE",
                           "AVERAGE \n FUEL \n CONSUPTION"])
        # Создаем таблицу
        self.logger.debug("Creating short statistics table")
        table = Table(table_data, repeatRows=True)
        table_style = self.s_table
        table.setStyle(TableStyle(table_style))
        self.logger.info("Short statistics table was created")
        elements.append(table)

        # Информация о самой часто посещаемой заправке
        self.logger.debug("Generating info about the most visited gas station")
        elements.append(Paragraph("The most visited gas station", self.s_header_2))
        table_data = self.table_data_to_list(
            self.db.select("v_trans v",
                           """
                           name,
                           price,
                           mpg,
                           mile_price,
                           (SELECT COUNT(vv.name) FROM v_trans vv WHERE vv.name = v.name AND """ +
                           self.condition + ") as names_count", condition=self.condition,
                           order_by="names_count DESC", limit="1"))

        table_data.insert(0, ["GAS \n STATION", "GALLON \n PRICE", "MPG",
                              "MILE \n PRICE", "VISITS"])
                
        table = Table(table_data, repeatRows=True)
        table_style = self.s_table
        table.setStyle(TableStyle(table_style))
        self.logger.info("Generated info about the most visited gas station")
        elements.append(table)

        # Информация о самой выгодной заправке
        self.logger.debug("Generating info about the most profitable gas station")
        elements.append(Paragraph("The most profitable gas station", self.s_header_2))
        table_data = self.table_data_to_list(
            self.db.select("v_trans",
                           """
                           name,
                           price,
                           mpg,
                           mile_price,
                           COUNT(name)
                           """,
                           self.condition + 
                           "AND price = (SELECT MIN(price) FROM v_trans WHERE "
                           + self.condition + ")",
                           limit="1"))

        table_data.insert(0, ["GAS \n STATION", "GALLON \n PRICE", "MPG",
                              "MILE \n PRICE", "VISITS"])
                
        table = Table(table_data, repeatRows=True)
        table_style = self.s_table
        table.setStyle(TableStyle(table_style))
        self.logger.info("Generated info about the most profitable gas station was generated")
        elements.append(table)
        elements.append(Spacer(0, 15))

        # Информация о том, сколько можно было съэкономить,
        # если бы человек заправлялся только на самой выгодной
        # заправке.
        # Общая цена заправок равна сумме цен заправок.
        # Общая цена заправок, если все заправки были бы
        # самыми выгодными равна:
        # цена одного галлона умноженная на общую сумму
        # всех купленных галлонов, затем разделить 100,
        # чтобы получить цену в галлонах.
        table_data = self.table_data_to_list(
            self.db.select("v_trans",
                           """
                           SUM(cost),
                           (SELECT price
                            FROM v_trans
                            WHERE price = (SELECT MIN(price) FROM v_trans WHERE """
                           + self.condition + ")) * SUM(amount) / 100", condition=self.condition))
        
        elements.append(Paragraph("Total spent " + 
                                  str(table_data[0][0]) + 
                                  "$ on gas stations.",
                                  self.s_text))
        elements.append(Paragraph("If you only refueled at the most " + 
                                  "profitable gas station, the price would be " +
                                  str(table_data[0][1]) + "$.",
                                  self.s_text))
        elements.append(Paragraph("So we get, that you could save " +
                                  str(round(table_data[0][0] - table_data[0][1], 2)) + "$.",
                                  self.s_text))              

        return elements



    def table_data_to_list(self, data):
        c = []
        for row in data:
            lst = []
            for e in row:
                if type(e) is float:
                    e = round(e, 2)
                lst.append(e)
            c.append(lst)
        return c