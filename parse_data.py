__all__ = ["get_data", "program_breakdown"]

from os import listdir, makedirs, path
import pandas as pd
import numpy as np


def get_data(my_path):
    """
    :param my_path: путь к папке стаблицами
    :return: таблица с данными, собранными из всех таблиц
    """
    if not path.exists(my_path + "/csv"):
        makedirs(my_path + "/csv")
    for name in listdir(my_path):
        ws = pd.read_excel(f"{my_path}/" + name)
        ws.to_csv(f"{my_path}/csv" + name + ".csv", encoding="cp1251", sep=';', index=False)
    students = pd.DataFrame()
    for name in listdir(my_path):
        students = students.append(func(name))
    return students


# Эта функция достаёт данные
def func(name):
    """
    :param name: название образовательной программы
    :return: таблица с необходимыми данными
    """
    # Достаём основную таблицу из файла CSV
    students = np.loadtxt(f"{path}/{name}",
                          delimiter=';',
                          skiprows=15,
                          encoding="cp1251",
                          dtype='O')
    # Достаём название образовательной программы
    text_mas = np.loadtxt(f"{path}/{name}",
                          delimiter=';',
                          skiprows=2,
                          encoding="cp1251",
                          max_rows=1,
                          dtype='O')
    napravlenie = str(text_mas)[29:-2]

    # print(Napravlenie)
    # Достаём количество бюджетных мест
    text_mas = np.loadtxt(f"{path}/{name}",
                          delimiter=';',
                          skiprows=7,
                          encoding="cp1251",
                          max_rows=1,
                          dtype='O')
    budget = int(text_mas[0][27:])
    # Достаём количество платных мест
    text_mas = np.loadtxt(f"{path}/{name}",
                          delimiter=';',
                          skiprows=9,
                          encoding="cp1251",
                          max_rows=1,
                          dtype='O')
    platno = int(text_mas[0][25:])

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
        x = np.append(x, napravlenie)
    students = np.c_[students, x]
    x = np.array("Бюджетные места")
    for i in range(num_of_stud, 1, -1):
        x = np.append(x, budget)
    students = np.c_[students, x]
    x = np.array("Платные места")
    for i in range(num_of_stud, 1, -1):
        x = np.append(x, platno)
    students = np.c_[students, x]
    # Запиливаем пандас датафрейм и название столбцов
    students = pd.DataFrame(students[1:, ], columns=students[0, ])
    return students


def program_breakdown(students, params="", programs=[]):
    """
    :param students: pandas.DataFrame, база данных
    :param params: string, 'q' - таблица по студентам, имеющим особое право,
                    'tq' - по целевой квоте, в противном случае по олимпиадам
    :param programs: list<string>, список образовательных программ
    :return: pandas.DataFrame, содержащий данные по выбраной категории
    """
    df = students[["Образовательная программа", "Заявление о согласии на зачисление", "Возврат документов",
                   "Литература", "Русский язык ЕГЭ", "Иностранный язык", "История ЕГЭ", "Математика ЕГЭ",
                   "Биология ЕГЭ",
                   "Химия", "Обществознание ЕГЭ", "Физика", "География", "Информатика", "Сумма конкурсных баллов",
                   "Творческий конкурс Медиа", "Творческий конкурс Мода", "Творческий конкурс I этап",
                   "Заявление о согласии на зачисление", "Возврат документов"]]
    if params == "q":
        column = "Поступление на места в рамках особой квоты для лиц, имеющих особое право"
    elif params == "tq":
        column = "Поступление на места по целевой квоте"
    else:
        column = "Право поступления без вступительных испытаний"
    df[column] = students[column]
    if programs:
        df = df["Образовательная программа"].loc[df["Образовательная программа"].isin(programs)]
    if params not in ["q", "tk"]:
        df[column] = df[column].fillna("-")
        df.loc[df[column] != "-", column] = "+"
    new_column = pd.pivot_table(df, index=["Образовательная программа"] + [column], values="Сумма конкурсных баллов",
                                aggfunc=len)
    new_column.rename(columns={"Сумма конкурсных баллов": "Количество поступающих"}, inplace=True)
    pt = pd.pivot_table(df, index=["Образовательная программа"] + [column])
    pt = pd.concat([pt, new_column], axis=1)
    return pt
