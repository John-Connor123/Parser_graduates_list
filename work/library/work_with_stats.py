__all__ = ['Places_for_education', 'Get_SNILS_by_exam', 'Students_Data', 'program_breakdown', 'save_file']
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from os import listdir, makedirs, path

"""def get_params_to_calculate(data, education_form=''):
'''    
    Возвращает промежуточные данные для расчётов.
    :param data: pandas-обьект с данными по приемной кампании.
    :param education_form: форма обучения.
    :return: список из суммы баллов по ЕГЭ для каждого абитуриента;
    список, содержащий информацию о том, подал ли заявление каждый абитуриент;
    кол-во олимпиадников; общее кол-во конкурсных мест.
    '''
    return final_scores, agreements, BVI_number, all_places


def get_stats(data, education_form=''):
    ''':param data: pandas-обьект с данными по приемной кампании
       :param education_form: форма обучения
       :return: средний балл и минимальный балл для платников'''
    final_scores, agreements, BVI_number, all_places = get_params_to_calculate(data, education_form=education_form)

    return avg_score_commerce, min_score_commerce
"""


def Get_SNILS_by_exam(students, exam, points, operator = '>'):
    '''
    :param students: pandas.DataFrame, База данных
    :param exam: string, Экзамен, по которому будет построена статистика
    :param points: integer, Количество баллов, относительно которого рассматривается статистика
    :param operator: char, '<', '>' или '='. Необходим для показа балов ниже, выше или равных порога (по умолчанию '>')
    :return: таблицу со СНИЛСами и данными по заданному экзамену, картинку с двумя графиками:
    круговой диаграммой и ящиком с усами
    '''
    counts = {"< " + str(points): 0, "= " + str(points): 0, "> " + str(points): 0}
    df = students[["СНИЛС", exam]]
    df = df[~df[exam].isnull()]
    df = df[df[exam] != ""]
    df[exam] = df[exam].astype(int)
    plt.subplot(2,1,2)
    df[[exam]].boxplot(grid = True, notch = True, showmeans = True, whis = 1.5, vert = False, showfliers = False)
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
    df.reset_index(inplace = True, drop = True)
    plt.subplot(2,1,1)
    plt.pie(counts.values(), labels = counts.keys())
    plt.title("Количество баллов по предмету " + exam)
    plt.ylabel("")
    return df, plt


def Places_for_education(students, programs, budget, paid, programStr = "Образовательная программа", budgetStr = "Бюджетные места", paidStr ="Платные места"):
    '''
    :param students: pandas.DataFrame, база данных
    :param programs: list<string>, список образовательных программ
    :param budget: char, '+' - сортировать по количеству бюджетных мест, '-' - не сортировать
    :param paid: char, '+' - сортировать по количеству бюджетных мест, '-' - не сортировать
    :param programStr: string, название столбца базы данных, в котором написаны названия образовательных программ
    :param budgetStr: string, название столбца базы данных, в котором написаны количества бюджетных мест
    :param paidStr: string, название столбца базы данных, в котором написаны количества платных мест
    :return: таблица с количеством платных и/или бюджетных мест по выбраным программам
    и столбчатую диаграмму с количеством платных и бюджетных мест по выбранным программам
    '''
    df = students[["Образовательная программа", "Бюджетные места", "Платные места"]]
    if budget == '-':
        if paid == '-':
            df = df[["Образовательная программа"]]
        else:
            df = df[["Образовательная программа", "Платные места"]]
    elif paid == '-':
        df = df[["Образовательная программа", "Бюджетные места"]]
    df = df.drop_duplicates(subset = "Образовательная программа", keep = "first")
    if programs:
        df = df.loc[df["Образовательная программа"].isin(programs)]
    df.reset_index(inplace = True, drop = True)
    df = df.set_index("Образовательная программа")
    hist1 = df.plot(figsize=(26,25),kind="bar")
    fig1 = hist1.get_figure()
    return df, fig1


def Students_Data(students,  without_exam, special_q, target_q, programs, points,
                  operator, without_examStr = "Право поступления без вступительных испытаний",
                  special_qStr = "Поступление на места в рамках особой квоты для лиц, имеющих особое право",
                  target_qStr = "Поступление на места по целевой квоте", programStr = "Образовательная программа",
                  points_sumStr = "Сумма конкурсных баллов"):
    '''
    :param students: pandas.DataFrame, база данных
    :param without_exam: char, '+' - сортировать по олимпиадам, '-' - не сортировать
    :param special_q: char, '+' - сортировать по специальной квоте, '-' - не сортировать
    :param target_q: char, '+' - сортировать по целевой квоте, '-' - не сортировать
    :param programs: list<string>, список образовательных программ
    :param points: integer, Количество баллов, относительно которого рассматривается статистика
    :param operator: char, '<', '>' или '='. Необходим для показа балов ниже, выше или равных порога (по умолчанию '>')
    :param without_examStr: string, название столбца базы данных, в котором написаны права на поступление по олимпиаде
    :param special_qStr: string, название столбца базы данных, в котором написаны права на поступление по специальной квоте
    :param target_qStr: string, название столбца базы данных, в котором написаны права на поступление по целевой квоте
    :param programStr: string, название столбца базы данных, в котором написаны названия образовательных программ
    :param points_sumStr: string, название столбца базы данных, в котором написаны суммы конкурсных баллов
    :return:
    '''
    df = students[["СНИЛС", without_examStr, special_qStr, target_qStr, programStr, points_sumStr]]
    df = df[~df[points_sumStr].isnull()]
    df = df[df[points_sumStr] != ""]
    df[points_sumStr] = df[points_sumStr].astype(int)
    if programs:
        buff = df[programStr].loc[~df[programStr].isin(programs)]
        df = df.loc[~df[programStr].isin(buff)]
    if operator == '<':
        df = df[df[points_sumStr] < points]
    elif operator == '=':
        df = df[df[points_sumStr] == points]
    else:
        df = df[df[points_sumStr] > points]
    df1 = df[["СНИЛС", programStr, points_sumStr]]
    if without_exam == '+':
        df1.loc[:,without_examStr] = df[without_examStr]
    if special_q == '+':
        df1.loc[:,special_qStr] = df[special_qStr]
    if target_q == '+':
        df1.loc[:, target_qStr] = df[target_qStr]
    return df1


def program_breakdown(students, params = "", programs = []):
    df = students[["Образовательная программа","Заявление о согласии на зачисление","Возврат документов",
                  "Литература","Русский язык ЕГЭ","Иностранный язык","История ЕГЭ","Математика ЕГЭ","Биология ЕГЭ",
                  "Химия","Обществознание ЕГЭ","Физика","География","Информатика","Сумма конкурсных баллов",
                  "Творческий конкурс Медиа","Творческий конкурс Мода","Творческий конкурс I этап",
                  "Заявление о согласии на зачисление","Возврат документов"]]
    if params == "q":
        column = "Поступление на места в рамках особой квоты для лиц, имеющих особое право"
    elif params == "tq":
        column = "Поступление на места по целевой квоте"
    else:
        column = "Право поступления без вступительных испытаний"
    df[column] = students[column]
    if programs:
        df = df["Образовательная программа"].loc[df["Образовательная программа"].isin(programs)]
    if params not in ["q","tk"]:
        df[column] = df[column].fillna("-")
        df.loc[df[column] != "-", column] = "+"
    new_column = pd.pivot_table(df, index = ["Образовательная программа"] + [column], values = "Сумма конкурсных баллов", aggfunc = len)
    new_column.rename(columns = {"Сумма конкурсных баллов": "Количество поступающих"}, inplace = True)
    pt = pd.pivot_table(df, index = ["Образовательная программа"] + [column])
    pt = pd.concat([pt,new_column], axis = 1)
    return pt, new_column


def save_file(file, file_name, path=""):
    if isinstance(file, pd.DataFrame):
        file.to_excel(path + file_name + ".xlsx")
    else:
        file.savefig(path + file_name + ".png")
