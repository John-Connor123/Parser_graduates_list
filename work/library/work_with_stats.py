__all__ = ['Places_for_education', 'Get_SNILS_by_exam', 'Students_Data', 'save_file']

import matplotlib.figure
import pandas as pd


def Get_SNILS_by_exam(students, exam, points, operator='>'):
    """
    :param students: pandas.DataFrame, База данных
    :param exam: string, Экзамен, по которому будет построена статистика
    :param points: integer, Количество баллов, относительно которого рассматривается статистика
    :param operator: string, '<', '>' или '='.
                    Необходим для отбора балов ниже, выше или равных порога (по умолчанию '>')
    :return: таблицу со СНИЛСами и данными по заданному экзамену, картинку с двумя графиками:
    круговой диаграммой и ящиком с усами
    """
    counts = {"< " + str(points): 0, "= " + str(points): 0, "> " + str(points): 0}
    data_frame = students[["СНИЛС", exam]]
    data_frame = data_frame[~data_frame[exam].isnull()]
    data_frame = data_frame[data_frame[exam] != ""]
    data_frame[exam] = data_frame[exam].astype(int)
    figure = matplotlib.figure.Figure(figsize = (10, 10), dpi = 100)
    plot = figure.add_subplot(212)
    plot.boxplot(data_frame[[exam]], notch = True, showmeans = True, whis = 1.5, vert = False, showfliers = False)
    for score in data_frame[exam]:
        if score < points:
            counts["< " + str(points)] += 1
        elif score == points:
            counts["= " + str(points)] += 1
        else:
            counts["> " + str(points)] += 1
    if operator == '<':
        data_frame = data_frame[data_frame[exam] < points]
    elif operator == '=':
        data_frame = data_frame[data_frame[exam] == points]
    else:
        data_frame = data_frame[data_frame[exam] > points]
    data_frame.reset_index(inplace = True, drop = True)
    plot1 = figure.add_subplot(211)
    plot1.pie(counts.values(), labels = counts.keys())
    return data_frame, figure


def Places_for_education(students, programs, budget, paid, program_str="Образовательная программа",
                         budget_str="Бюджетные места", paid_str="Платные места"):
    """
    :param students: pandas.DataFrame, база данных
    :param programs: list<string>, список образовательных программ
    :param budget: char, '+' - сортировать по количеству бюджетных мест, '-' - не сортировать
    :param paid: char, '+' - сортировать по количеству бюджетных мест, '-' - не сортировать
    :param program_str: string, название столбца базы данных c названиями образовательных программ
    :param budget_str: string, название столбца базы данных с количествами бюджетных мест
    :param paid_str: string, название столбца базы данных с количествами платных мест
    :return: таблица с количеством платных и/или бюджетных мест по выбраным программам
    и столбчатая диаграмма с количеством платных и бюджетных мест по выбранным программам
    """
    data_frame = students[[program_str, budget_str, paid_str]]
    if budget == '-':
        if paid == '-':
            data_frame = data_frame[[program_str]]
        else:
            data_frame = data_frame[[program_str, paid_str]]
    elif paid == '-':
        data_frame = data_frame[[program_str, budget_str]]
    data_frame = data_frame.drop_duplicates(subset=program_str, keep="first")
    if programs:
        data_frame = data_frame.loc[data_frame[program_str].isin(programs)]
    data_frame.reset_index(inplace=True, drop=True)
    data_frame = data_frame.set_index(program_str)
    bar_graph = data_frame.plot(figsize=(26, 25), kind="bar")
    figure = bar_graph.get_figure()
    return data_frame, figure


def Students_Data(students, without_exam, special_quota, target_quota, programs, points,
                  operator, without_exam_str="Право поступления без вступительных испытаний",
                  special_quota_str=
                  "Поступление на места в рамках особой квоты для лиц, имеющих особое право",
                  target_quota_str="Поступление на места по целевой квоте",
                  program_str="Образовательная программа",
                  points_sum_str="Сумма конкурсных баллов"):
    """
    :param students: pandas.DataFrame, база данных
    :param without_exam: string, '+' - сортировать по олимпиадам, '-' - не сортировать
    :param special_quota: string, '+' - сортировать по специальной квоте, '-' - не сортировать
    :param target_quota: string, '+' - сортировать по целевой квоте, '-' - не сортировать
    :param programs: list<string>, список образовательных программ
    :param points: int, Количество баллов, относительно которого рассматривается статистика
    :param operator: string, '<', '>' или '='. Необходим для показа балов относительно порога
    :param without_exam_str: string, название столбца с данными о студентах
    с правом на поступление по олимпиаде
    :param special_quota_str:string, название столбца с данными о студентах
    с правом на поступление по специальной квоте
    :param target_quota_str: string, название столбца с данными о студентах
    с правом на поступление по целевой квоте
    :param program_str: string, название столбца базы данных с названиями образовательных программ
    :param points_sum_str: string, название столбца базы данных с суммами конкурсных баллов
    :return: таблицу, содержащую данные о студентах, поступающих по олимпиадам и/или квоте
    """
    data_frame = students[["СНИЛС", without_exam_str, special_quota_str,
                   target_quota_str, program_str, points_sum_str]]
    data_frame = data_frame[~data_frame[points_sum_str].isnull()]
    data_frame = data_frame[data_frame[points_sum_str] != ""]
    data_frame[points_sum_str] = data_frame[points_sum_str].astype(int)
    if programs:
        buff = data_frame[program_str].loc[~data_frame[program_str].isin(programs)]
        data_frame = data_frame.loc[~data_frame[program_str].isin(buff)]
    if operator == '<':
        data_frame = data_frame[data_frame[points_sum_str] < points]
    elif operator == '=':
        data_frame = data_frame[data_frame[points_sum_str] == points]
    else:
        data_frame = data_frame[data_frame[points_sum_str] > points]
    df1 = data_frame[["СНИЛС", program_str, points_sum_str]]
    if without_exam == '+':
        df1.loc[:, without_exam_str] = data_frame[without_exam_str]
    if special_quota == '+':
        df1.loc[:, special_quota_str] = data_frame[special_quota_str]
    if target_quota == '+':
        df1.loc[:, target_quota_str] = data_frame[target_quota_str]
    return df1


def save_file(file, file_name, path=""):
    """
    :param file: string, переменная, содержащая данные, которые необходимо сохранить
    :param file_name: string, имя для будущего файла. Без расширения
    :param path: string, путь к папке для сохранения файла
    :return: файл в формате .png или .xlsx
    """
    if isinstance(file, pd.DataFrame):
        file.to_excel(path + file_name + ".xlsx")
    elif isinstance(file, matplotlib.figure.Figure):
        file.savefig(path + file_name + ".png")
