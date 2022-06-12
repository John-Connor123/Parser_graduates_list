__all__ = ['places_for_education', 'get_snils_by_exam', 'students_data', 'save_file']

import matplotlib.figure
import pandas as pd
import matplotlib.pyplot as plt


def get_snils_by_exam(students, exam, points, operator='>'):
    """
    :param students: pandas.DataFrame, База данных
    :param exam: string, Экзамен, по которому будет построена статистика
    :param points: integer, Количество баллов, относительно которого рассматривается статистика
    :param operator: char, '<', '>' или '='. Необходим для показа балов ниже, выше или равных порога (по умолчанию '>')
    :return: таблицу со СНИЛСами и данными по заданному экзамену, картинку с двумя графиками:
    круговой диаграммой и ящиком с усами
    """
    counts = {"< " + str(points): 0, "= " + str(points): 0, "> " + str(points): 0}
    df = students[["СНИЛС", exam]]
    df = df[~df[exam].isnull()]
    df = df[df[exam] != ""]
    df[exam] = df[exam].astype(int)
    plt.subplot(2, 1, 2)
    df[[exam]].boxplot(grid=True, notch=True, showmeans=True, whis=1.5, vert=False, showfliers=False)
    for score in df[exam]:
        if score < points:
            counts["< " + str(points)] += 1
        elif score == points:
            counts["= " + str(points)] += 1
        else:
            counts["> " + str(points)] += 1
    if operator == '<':
        df = df[df[exam] < points]
    elif operator == '=':
        df = df[df[exam] == points]
    else:
        df = df[df[exam] > points]
    df.reset_index(inplace=True, drop=True)
    plt.subplot(2, 1, 1)
    plt.pie(counts.values(), labels=counts.keys())
    plt.title("Количество баллов по предмету " + exam)
    plt.ylabel("")
    return df, plt


def places_for_education(students, programs, budget, paid, program_str="Образовательная программа",
                         budget_str="Бюджетные места", paid_str="Платные места"):
    """
    :param students: pandas.DataFrame, база данных
    :param programs: list<string>, список образовательных программ
    :param budget: char, '+' - сортировать по количеству бюджетных мест, '-' - не сортировать
    :param paid: char, '+' - сортировать по количеству бюджетных мест, '-' - не сортировать
    :param program_str: string, название столбца базы данных, в котором написаны названия образовательных программ
    :param budget_str: string, название столбца базы данных, в котором написаны количества бюджетных мест
    :param paid_str: string, название столбца базы данных, в котором написаны количества платных мест
    :return: таблица с количеством платных и/или бюджетных мест по выбраным программам
    и столбчатую диаграмму с количеством платных и бюджетных мест по выбранным программам
    """
    df = students[[program_str, budget_str, paid_str]]
    if budget == '-':
        if paid == '-':
            df = df[[program_str]]
        else:
            df = df[[program_str, paid_str]]
    elif paid == '-':
        df = df[[program_str, budget_str]]
    df = df.drop_duplicates(subset=program_str, keep="first")
    if programs:
        df = df.loc[df[program_str].isin(programs)]
    df.reset_index(inplace=True, drop=True)
    df = df.set_index(program_str)
    hist1 = df.plot(figsize=(26, 25), kind="bar")
    fig1 = hist1.get_figure()
    return df, fig1


def students_data(students, without_exam, special_q, target_q, programs, points,
                  operator, without_exam_str="Право поступления без вступительных испытаний",
                  special_quota_str="Поступление на места в рамках особой квоты для лиц, имеющих особое право",
                  target_quota_str="Поступление на места по целевой квоте", program_str="Образовательная программа",
                  points_sum_str="Сумма конкурсных баллов"):
    """
    :param students: pandas.DataFrame, база данных
    :param without_exam: string, '+' - сортировать по олимпиадам, '-' - не сортировать
    :param special_q: string, '+' - сортировать по специальной квоте, '-' - не сортировать
    :param target_q: string, '+' - сортировать по целевой квоте, '-' - не сортировать
    :param programs: list<string>, список образовательных программ
    :param points: integer, Количество баллов, относительно которого рассматривается статистика
    :param operator: string, '<', '>' или '='. Необходим для показа балов ниже, выше или равных порога
    :param without_exam_str: string, название столбца с данными о студентах с правом на поступление по олимпиаде
    :param special_quota_str:string, название столбца с данными о студентах с правом на поступление по специальной квоте
    :param target_quota_str: string, название столбца с данными о студентах с правом на поступление по целевой квоте
    :param program_str: string, название столбца базы данных, в котором написаны названия образовательных программ
    :param points_sum_str: string, название столбца базы данных, в котором написаны суммы конкурсных баллов
    :return:
    """
    df = students[["СНИЛС", without_exam_str, special_quota_str, target_quota_str, program_str, points_sum_str]]
    df = df[~df[points_sum_str].isnull()]
    df = df[df[points_sum_str] != ""]
    df[points_sum_str] = df[points_sum_str].astype(int)
    if programs:
        buff = df[program_str].loc[~df[program_str].isin(programs)]
        df = df.loc[~df[program_str].isin(buff)]
    if operator == '<':
        df = df[df[points_sum_str] < points]
    elif operator == '=':
        df = df[df[points_sum_str] == points]
    else:
        df = df[df[points_sum_str] > points]
    df1 = df[["СНИЛС", program_str, points_sum_str]]
    if without_exam == '+':
        df1.loc[:, without_exam_str] = df[without_exam_str]
    if special_q == '+':
        df1.loc[:, special_quota_str] = df[special_quota_str]
    if target_q == '+':
        df1.loc[:, target_quota_str] = df[target_quota_str]
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
