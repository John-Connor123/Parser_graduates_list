# -*- coding: utf-8 -*-
"""
Created on Fri May  6 15:31:38 2022

@author: Умелец
"""
from os import listdir
import pandas as pd
import numpy as np
import openpyxl


#Эта функция достаёт данные
def function(name):
    #Достаём основную таблицу из файла CSV
    students = np.loadtxt(f'D:/VUZD/PythonBD/Data_csv/{name}',
                          delimiter = ';',
                          skiprows = 15,
                          encoding = 'cp1251',
                          dtype = 'O')
    #Достаём название образовательной программы
    Text_mas = np.loadtxt(f'D:/VUZD/PythonBD/Data_csv/{name}',
                          delimiter = ';',
                          skiprows = 2,
                          encoding = 'cp1251',
                          max_rows = 1,
                          dtype = 'O')
    Napravlenie = str(Text_mas)[28:-1]

    #Достаём количество бюджетных мест
    Text_mas = np.loadtxt(f'D:/VUZD/PythonBD/Data_csv/{name}',
                          delimiter = ';',
                          skiprows = 7,
                          encoding = 'cp1251',
                          max_rows = 1,
                          dtype = 'O')
    Budget = int(Text_mas[0][27:])
    #Достаём количество платных мест
    Text_mas = np.loadtxt(f'D:/VUZD/PythonBD/Data_csv/{name}',
                          delimiter = ';',
                          skiprows = 9,
                          encoding = 'cp1251',
                          max_rows = 1,
                          dtype = 'O')
    Platno = int(Text_mas[0][25:])

    #Очистка от пустых столбцов
    for i in range(students.shape[1]-1,0,-1):
        if students[0,i] == '':
            students = np.delete(students, i, 1)
    #Вставляем соответствующие столбцы
    num_of_stud = 0
    for i in students:
        num_of_stud+=1
    x = np.array("Образовательная программа")
    for i in range(num_of_stud,1,-1):
        x = np.append(x, Napravlenie)
    students = np.c_[students, x]
    x = np.array("Бюджетные места")
    for i in range(num_of_stud,1,-1):
        x = np.append(x, Budget)
    students = np.c_[students, x]
    x = np.array("Платные места")
    for i in range(num_of_stud,1,-1):
        x = np.append(x, Platno)
    students = np.c_[students, x]
    #Запиливаем пандас датафрейм и название столбцов
    students = pd.DataFrame(students[1:,],columns = students[0,])
    return students

#Достаём данные из всех файлов и склеиваем их в одну кучку
students = pd.DataFrame()
for name in listdir('D:/VUZD/PythonBD/Data_csv/'):
    students = students.append(function(name))
    
#А здесь я начинаю искать нужные мне данные

def entrant(x):
    m = students[["№ п/п", "СНИЛС", "Право поступления без вступительных испытаний", "Поступление на места в рамках особой квоты для лиц, имеющих особое право", "Поступление на места по целевой квоте", "Образовательная программа", "Сумма конкурсных баллов"]]
    m = m.loc[m['СНИЛС'] == x]
    m.to_excel('D:/VUZD/PythonBD/Example7.xlsx', na_rep='')
    return(m)

def Get_SNILS_by_exam(exam, points, operator):
    m = students[["СНИЛС", exam]] 
    m = m[~m.exam.isnull()]
    m = m[m.exam != ""]
    m.exam = m.exam.astype(int)
    if operator == '>':
        m = m[m.exam > points]
    elif operator == '<':
        m = m[m.exam < points]
    elif operator == '=':
        m = m[m.exam == points]
    elif operator == '<=':
        m = m[m.exam <= points]
    elif operator == '>=':
        m = m[m.exam >= points]
    else:
        m = m[m.exam > points]
    m.reset_index(inplace = True, drop = True)
    m.to_excel('D:/VUZD/PythonBD/Example1.xlsx', na_rep='')
    return (m)

def Places_for_education(name, budget, paid):
    m = students[["Образовательная программа", "Бюджетные места", "Платные места"]] 
    m = m.drop_duplicates(subset = 'Образовательная программа', keep = 'first')
    m.reset_index(inplace = True, drop = True)
    if name == 'all':
        if budget == '+':
            m = m[m["Бюджетные места"] != "0"]
        elif budget == '-':
            m = m[m["Бюджетные места"] == "0"]
        if paid == '+':
            m = m[m["Платные места"] != "0"]
        elif paid == '-':
            m = m[m["Платные места"] == "0"]
        return (m)
    else:
        m = m[m["Образовательная программа"] == name]
        if budget == '+':
            m = m[m["Бюджетные места"] != "0"]
        elif budget == '-':
            m = m[m["Бюджетные места"] == "0"]
        if paid == '+':
            m = m[m["Платные места"] != "0"]
        elif paid == '-':
            m = m[m["Платные места"] == "0"]
        return (m)
    m.to_excel('D:/VUZD/PythonBD/Example2.xlsx', na_rep='')
    


m = students[['№ п/п','Заявление о согласии на зачисление','Право поступления без вступительных испытаний','Поступление на места в рамках особой квоты для лиц, имеющих особое право','Поступление на места по целевой квоте','Сумма конкурсных баллов','Возврат документов','Образовательная программа','Бюджетные места','Платные места',"История ЕГЭ", "История ЕГЭ",	"Математика ЕГЭ",	"Биология ЕГЭ",	"Химия",	"Обществознание ЕГЭ", 	"Творческий конкурс Дизайн",	"Физика",	"География",	"Информатика", "Литература",	"Русский язык ЕГЭ",	"Иностранный язык"]]
m = m.loc[m['Заявление о согласии на зачисление'] == '+']
m = m.loc[m['Право поступления без вступительных испытаний'] == '']
m = m.loc[m['Возврат документов'] == '-']
m["Quota"] = np.where((m["Поступление на места по целевой квоте"] == "+")|(m["Поступление на места в рамках особой квоты для лиц, имеющих особое право"] == "+"), "Quota", "No quota")
m.drop(["Поступление на места по целевой квоте", "Поступление на места в рамках особой квоты для лиц, имеющих особое право", "Право поступления без вступительных испытаний", 'Возврат документов', 'Заявление о согласии на зачисление', "№ п/п", "Бюджетные места", "Платные места", 'Сумма конкурсных баллов'], axis = 1, inplace = True)
m = pd.melt(m, id_vars=['Образовательная программа', 'Quota'], value_vars=['История ЕГЭ','История ЕГЭ', 'Математика ЕГЭ', 'Биология ЕГЭ', 'Химия','Обществознание ЕГЭ', 'Творческий конкурс Дизайн', 'Физика','География', 'Информатика', 'Литература', 'Русский язык ЕГЭ','Иностранный язык'])
m.value[m.value == ""] = 0
m["value"] = m.value.astype(float)
n = pd.pivot_table(m, values='value', index=['Образовательная программа', 'Quota'],columns = ['variable'], aggfunc=np.mean)
n.to_excel('D:/VUZD/PythonBD/Example5.xlsx', na_rep='')



m = students[['№ п/п','Заявление о согласии на зачисление','Право поступления без вступительных испытаний','Поступление на места в рамках особой квоты для лиц, имеющих особое право','Поступление на места по целевой квоте','Сумма конкурсных баллов','Возврат документов','Образовательная программа','Бюджетные места','Платные места',"История ЕГЭ", "История ЕГЭ",	"Математика ЕГЭ",	"Биология ЕГЭ",	"Химия",	"Обществознание ЕГЭ", 	"Творческий конкурс Дизайн",	"Физика",	"География",	"Информатика", "Литература",	"Русский язык ЕГЭ",	"Иностранный язык"]]
m = m.loc[m['Заявление о согласии на зачисление'] == '+']
m = m.loc[m['Поступление на места по целевой квоте'] == '-']
m = m.loc[m['Поступление на места в рамках особой квоты для лиц, имеющих особое право'] == '-']
m = m.loc[m['Возврат документов'] == '-']
m["Right_to_no_exams"] = np.where((m['Право поступления без вступительных испытаний'] != ""), "No_exams", "No_right")
m.drop(["Поступление на места по целевой квоте", "Поступление на места в рамках особой квоты для лиц, имеющих особое право", "Право поступления без вступительных испытаний", 'Возврат документов', 'Заявление о согласии на зачисление', "№ п/п", "Бюджетные места", "Платные места", 'Сумма конкурсных баллов'], axis = 1, inplace = True)
m = pd.melt(m, id_vars=['Образовательная программа', 'Right_to_no_exams'], value_vars=['История ЕГЭ','История ЕГЭ', 'Математика ЕГЭ', 'Биология ЕГЭ', 'Химия','Обществознание ЕГЭ', 'Творческий конкурс Дизайн', 'Физика','География', 'Информатика', 'Литература', 'Русский язык ЕГЭ','Иностранный язык'])
m.value[m.value == ""] = 0
m["value"] = m.value.astype(float)
n = pd.pivot_table(m, values='value', index=['Образовательная программа', 'Right_to_no_exams'],columns = ['variable'], aggfunc=np.mean)
n.to_excel('D:/VUZD/PythonBD/Example6.xlsx', na_rep='')















def To_Bot(SNILS):
    all_students_df = students[["№ п/п", "СНИЛС", "Право поступления без вступительных испытаний", "Поступление на места в рамках особой квоты для лиц, имеющих особое право", "Поступление на места по целевой квоте", "Образовательная программа", "Сумма конкурсных баллов", "Заявление о согласии на зачисление","Бюджетные места"]]
    only_me_df = all_students_df.loc[all_students_df["СНИЛС"] == SNILS]
    
    desired_values = []
    for program_name, budget_places in zip(only_me_df["Образовательная программа"].tolist(), only_me_df["Бюджетные места"].tolist()):
        me_in_this_program = all_students_df[(all_students_df["Образовательная программа"] == program_name)&(all_students_df["СНИЛС"] == SNILS)]
        if me_in_this_program["Заявление о согласии на зачисление"].values[0] == "-":
            desired_values.append("-")
        else:
            one_prog_students_df = all_students_df[(all_students_df["Образовательная программа"] == program_name)]
            agreed_one_prog_students_df = one_prog_students_df[one_prog_students_df["Заявление о согласии на зачисление"] == "+"]
            agreed_one_prog_students_df.reset_index(inplace = True, drop = True)
            my_number = agreed_one_prog_students_df[agreed_one_prog_students_df["СНИЛС"] == SNILS].index[0]        
            if int(budget_places) - int(my_number) >= 0:
                desired_values.append("+")
            else: 
                desired_values.append("-")
    only_me_df.loc[:, "NewValue"] = desired_values
    only_me_dict = only_me_df.T.to_dict()
    only_me_dict = list(only_me_dict.values())
    return(only_me_dict)
    

#p = To_Bot(SNILS)
































