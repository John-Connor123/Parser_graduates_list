__all__ = ['get_params_to_calculate', 'get_stats']
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from os import listdir, makedirs, path

def get_params_to_calculate(data, education_form=''):
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

def Get_SNILS_by_exam(students, exam, points, operator):
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