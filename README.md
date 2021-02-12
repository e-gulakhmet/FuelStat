# FuelStat
A program that expands fuel statistics

![GitHub Logo](/images/logo.png)


**Задача из книги Чарльза Уэзерелла "Этюды для программистов".**

**Горючие слезы, или Учет расхода бензина**

Задача состоит в том, чтобы привести статистику,
исходя из созданных пользователем таблиц.

# Основные условия:

Известно, что каждой новой записи в журнале соответсвует
новая **полная заправка**. Исходя из этого можно сказать,
что количество галлонов, которые он покупает на новой заправке
показывают, сколько галлонов он потратил после прошлой заправки
Следовательно в строке с новой заправкой
указывается расстояние пройденное до новой заправки и 
количество галлонов, которые были потрачены после
предыдущей заправки. А цена голона и цена купленных голонов с
новой заправки. 

# Реализация:

В программе реализованны три модуля:

1. Создание базы данных, содержащей таблицы fuel и trans.
2. Загрузка данных из файлов csv в таблицы базы данных. Дублирование
данных разрешено.
3. Формирование отчета по использования топлива.

- В директории [`web`](web/) содержиться flask веб приложение, при помощи которого можно взаимодействовать с данными.

## Установка всех модулей и библиотек:

```
$ pip install -r requirements.txt
```

## Создание базы данных:

Для создания или пересоздания базы данных необходимо запустить это:

```
$ python main.py --recreate
```

## Загрузка данных

Для загрузку данных из файлов необходимо:

1. Создать каталог data в рабочем каталоге программы.

2. Представить данные для загрузки в файлы fuel.csv и trans.csv в каталог data

3. Файл fuel.csv имеет следующую структуру(Название заправки:str,цена:float)

4. Файл trans.csv имеет следующую структуру(дата:YY/MM/DD,расстояние пройденное автомобилем:int,название заправки:str,количество галлонов:float)

5. Запустить:

```
$ python main.py --load
```

## Формирование отчета

Отчет формируется в виде pdf-файла.

Для формирования отчета нужно запустить программу со следующими мараметрами:

```
$ python main.py --report -s start_data -e end_data -S start_odometer -D end_odometer -n gas_name -i info -s statistic -f file_name
```

- `start_date` -- Дата, с которой будет формироваться отчет.(string)

- `end_date` -- Дата, которой будет заканчиваться отчет.(string)

- `start_odometer` -- Пробег, с которого будет формироваться отчет.(integer)

- `end_odometer` -- Пробег, которым будет закачиваться отчет.(integer)

- `gas_name` -- Название заправки, по которой будет формироваться отчет(string). Если данный параметр вызвается несколько раз с разными названиями заправок, то отчет будет формироваться по этим названиям.
- `info` -- Если данный параметр был указан, то в отчете будет показана таблица.

- `statisctic` -- Если данный параметр был указан, то в отчете будет показана статистика.

- `file_name` -- Название файла с созданным отчетом.(string)


# Данные получаемые в отчете:

Отчет формируется по данным, даты которых входят в диапазон дат, указаных при запуске программы.

## Данные таблицы:

- Дата заправки.
- Название заправки.
- Расстояние пройденное до этой заправки(мили).
- Цена одного галлона(центы).
- Расстояние, пройденное после предыдущей заправки(мили).
- Количество галлонов.
- Общая стоимость заправки(доллары).
- Расстояние пройденно на одном галлоне(мили).
- Цена одной мили(доллары).
- Цена одного дня(доллары).

## Данные статистики:

### В основной таблице:

- Общее пройденное расстояние(мили).
- Среднее расстояние между заправками(мили).
- Средняя цена галлона(центы).
- Среднее количество галлонов.
- Средняя цена одной заправки(доллары).
- Общая цена всех заправок(доллары).
- Средний пробег на одном галлоне(мили).
- Средняя цена одной мили(доллары).
- Средний расход топлива(галлоны).

### В дополнительных таблицах:

- Самая часто посещаемая вами заправка.
- Самая выгодная заправка и информация о ней.
- Количество долларов, которые можно было сэкономить, если заправляться только на самой выгодной заправке.