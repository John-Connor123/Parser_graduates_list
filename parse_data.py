__all__ = ["get_data"]
from os import listdir, makedirs, path
import pandas as pd
import numpy as np

def get_data(my_path):
    '''
    :param my_path: путь к папке стаблицами
    :return: таблица с данными, собранными из всех таблиц
    '''
    if not path.exists(my_path + "/csv"):
        makedirs(my_path + "/csv")
    for name in listdir(my_path):
        WS = pd.read_excel(f"{my_path}/" + name)
        WS.to_csv(f"{my_path}/csv" + name + ".csv", encoding="cp1251", sep = ';', index = False)
    students = pd.DataFrame()
    for name in listdir(my_path):
        students = students.append(func(name))
    return students

def get_data(my_path, file_name):
    '''
    :param my_path: путь к папке стаблицами
    :param file_name: название xcls файла, в который будет записана полученная база данных
    :return: таблица с данными, собранными из всех таблиц
    '''
    df = get_data(my_path)
    df.to_excel(f"{my_path}/{file_name}.xlsx")
    return df

# Эта функция достаёт данные
def func(name):
    '''
    :param name: название образовательной программы
    :return: таблица с необходимыми данными
    '''
    # Достаём основную таблицу из файла CSV
    students = np.loadtxt(f"{path}/{name}",
                          delimiter=';',
                          skiprows=15,
                          encoding="cp1251",
                          dtype='O')
    # Достаём название образовательной программы
    Text_mas = np.loadtxt(f"{path}/{name}",
                          delimiter=';',
                          skiprows=2,
                          encoding="cp1251",
                          max_rows=1,
                          dtype='O')
    Napravlenie = str(Text_mas)[29:-2]

    # print(Napravlenie)
    # Достаём количество бюджетных мест
    Text_mas = np.loadtxt(f"{path}/{name}",
                          delimiter=';',
                          skiprows=7,
                          encoding="cp1251",
                          max_rows=1,
                          dtype='O')
    Budget = int(Text_mas[0][27:])
    # Достаём количество платных мест
    Text_mas = np.loadtxt(f"{path}/{name}",
                          delimiter=';',
                          skiprows=9,
                          encoding="cp1251",
                          max_rows=1,
                          dtype='O')
    Platno = int(Text_mas[0][25:])

    # Очистка от пустых столбцов
    for i in range(students.shape[1] - 1, 0, -1):
        if students[0, i] == '':
            students = np.delete(students, i, 1)
    # Вставляем соответствующие столбцы
    num_of_stud = 0
    for i in students:
        num_of_stud += 1
    x = np.array("Образовательная программа")
    for i in range(num_of_stud, 1, -1):
        x = np.append(x, Napravlenie)
    students = np.c_[students, x]
    x = np.array("Бюджетные места")
    for i in range(num_of_stud, 1, -1):
        x = np.append(x, Budget)
    students = np.c_[students, x]
    x = np.array("Платные места")
    for i in range(num_of_stud, 1, -1):
        x = np.append(x, Platno)
    students = np.c_[students, x]
    # Запиливаем пандас датафрейм и название столбцов
    students = pd.DataFrame(students[1:, ], columns=students[0,])
    return students
