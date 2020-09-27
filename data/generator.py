import csv
import random



def main():
    gas_name = ["Texaco", "Arco", "Shell", "Mobil",
                "Chevron", "DX", "Conoco", "American",
                "Phillips", "Ericson", "Exxon"]
    
    random.seed(10)

    # Создаем список, в который добавим созданные далее словари
    lst = []
    y = 2000
    m = 1
    d = 1
    odometer = 4000
    name = "Texaco"
    amount = 13.1
    data = {"dtime": "2000-00-00", "odometer": 4000, "name": "Texaco", "amount": 13.1}
    for i in range(0, 60):
        # Создаем строку с датой тразакции
        d += random.randint(0, 5)
        if (d > 31):
            d = 1
            m += 1
        if (m > 12):
            y += 1
        
        # Увеличиваем пройденное расстояение
        odometer += random.randint(50, 600)
        name = gas_name[random.randint(0, len(gas_name) - 1)]
        amount = "%.1f" % random.uniform(0, 15)
        # Ставим нули перед значением месяца и дня, если они меньше 10
        # Для получения вида: YYYY-MM-DD
        str_d = str(d)
        str_m = str(m)
        if d < 10:
            str_d = '0' + str(d)
        if m < 10:
            str_m = '0' + str(m)
        
        lst.append({"dtime": str(y) + '-' + str_m + '-' + str_d,
                    "odometer": odometer,
                    "name": name,
                    "amount": amount})

    with open('data/trans.csv', 'w', newline='') as csvfile:
        # Задаем столбцы, в которые будем заносить данные
        fieldnames = ["dtime", "odometer", "name", "amount"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        for d in lst:
            writer.writerow(d)



if __name__ == "__main__":
    main()
