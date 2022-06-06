__all__ = ['plt_params', 'Get_SNILS_by_exam']
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
def plt_params():
    params = {'axes.titlesize': 16,
              'legend.fontsize': 16,
              'figure.figsize': (8, 8),
              'axes.labelsize': 16,
              'xtick.labelsize': 16,
              'ytick.labelsize': 16,
              'figure.titlesize': 22}
    plt.rcParams.update(params)
    plt.style.use('seaborn-whitegrid')
    sns.set_style("white")

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
    df = students[[programStr, budgetStr, paidStr]]
    if budget == '-':
        if paid == '-':
            df = df[[programStr]]
        else:
            df = df[[programStr, paidStr]]
    elif paid == '-':
        df = df[[programStr, budgetStr]]
    df = df.drop_duplicates(subset = programStr, keep = "first")
    if programs:
        buff = df[programStr].loc[~df[programStr].isin(programs)] #Я не знаю, как сделать иначе
        df = df.loc[~df[programStr].isin(buff)]
    df.reset_index(inplace = True, drop = True)
    df.plot(x = programStr, kind = "bar", title = "Количество мест на выбранных программах", figsize = (20,9))
    return df, plt

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