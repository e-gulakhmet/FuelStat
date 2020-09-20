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
    for i in range(0, 20):
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
        amount = random.uniform(0, 15)
        lst.append({"dtime": str(y) + '-' + str(m) + '-' + str(d),
                    "odometer": odometer,
                    "name": name,
                    "amount": amount})

    with open('trans.csv', 'w', newline='') as csvfile:
        # Задаем столбцы, в которые будем заносить данные
        fieldnames = ["dtime", "odometer", "name", "amount"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        for d in lst:
            writer.writerow(d)



if __name__ == "__main__":
    main()
