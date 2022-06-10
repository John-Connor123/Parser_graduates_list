# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 00:49:31 2022

@author: Умелец
"""

from os import listdir
import pandas as pd
import numpy as np

import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk

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







def entrant_data(without_exam, special_q, target_q, ed_progaram, points, operator):
    m = students[["№ п/п", "СНИЛС", 
                 "Право поступления без вступительных испытаний", 
                 "Поступление на места в рамках особой квоты для лиц, имеющих особое право", 
                 "Поступление на места по целевой квоте", "Образовательная программа", 
                 "Сумма конкурсных баллов"]]
    ed_progaram = '"' + ed_progaram + '"'
    if without_exam == "1":
        m = m[m["Право поступления без вступительных испытаний"] != ""]
    if without_exam == "0":
        m = m[m["Право поступления без вступительных испытаний"] == ""]       
    if special_q == "1":
        m = m[m["Поступление на места в рамках особой квоты для лиц, имеющих особое право"] == "+"]
    if special_q == "0":
        m = m[m["Поступление на места в рамках особой квоты для лиц, имеющих особое право"] == "-"]   
    if target_q == "1":
        m = m[m["Поступление на места по целевой квоте"] == "+"]
    if target_q == "0":
        m = m[m["Поступление на места по целевой квоте"] == "-"]       
    if ed_progaram in m["Образовательная программа"].values:
        m = m[m["Образовательная программа"] == ed_progaram]   
    try:
        points = int(points)
    except ValueError:
        error_of_int = True
    else:
        error_of_int = False  
    if error_of_int == False:
            m.loc[m["Сумма конкурсных баллов"] == "", "Сумма конкурсных баллов"] = 0
            m.loc[:, "Сумма конкурсных баллов"] = m["Сумма конкурсных баллов"].astype(int)
            if operator == '>':
                m = m[m["Сумма конкурсных баллов"] > points]
            elif operator == '<':
                m = m[m["Сумма конкурсных баллов"] < points]
            elif operator == '=':
                m = m[m["Сумма конкурсных баллов"] == points]
            elif operator == '<=':
                m = m[m["Сумма конкурсных баллов"] <= points]
            elif operator == '>=':
                m = m[m["Сумма конкурсных баллов"] >= points]
            elif operator == '<>':
                m = m[m["Сумма конкурсных баллов"] != points]
            elif operator == '<>=':
                pass
            else:
                m = m[m["Сумма конкурсных баллов"] > points]     
    m.to_excel('D:/VUZD/PythonBD/Example7.xlsx', na_rep='')
    return(m)



def Get_SNILS_by_exam(exam, points, operator):
    m = students[["СНИЛС", exam]] 
    m = m[~m[exam].isnull()]
    m = m[m[exam] != ""]
    m[exam] = m[exam].astype(int)
    if operator == '>':
        m = m[m[exam] > points]
    elif operator == '<':
        m = m[m[exam] < points]
    elif operator == '=':
        m = m[m[exam] == points]
    elif operator == '<=':
        m = m[m[exam] <= points]
    elif operator == '>=':
        m = m[m[exam] >= points]
    elif operator == '>=<':
        pass
    else:
        m = m[m[exam] > points]
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
    

def quota_program_breakdown():
    m = students[['№ п/п','Заявление о согласии на зачисление',
                  'Право поступления без вступительных испытаний',
                  'Поступление на места в рамках особой квоты для лиц, имеющих особое право',
                  'Поступление на места по целевой квоте',
                  'Сумма конкурсных баллов','Возврат документов',
                  'Образовательная программа','Бюджетные места',
                  'Платные места',"История ЕГЭ", "История ЕГЭ",	
                  "Математика ЕГЭ",	"Биология ЕГЭ",	"Химия",	
                  "Обществознание ЕГЭ", 	"Творческий конкурс Дизайн",	
                  "Физика",	"География",	
                  "Информатика", "Литература",
                  "Русский язык ЕГЭ",
                  "Иностранный язык"]]
    m = m.loc[m['Заявление о согласии на зачисление'] == '+']
    m = m.loc[m['Право поступления без вступительных испытаний'] == '']
    m = m.loc[m['Возврат документов'] == '-']
    m["Quota"] = np.where((m["Поступление на места по целевой квоте"] == "+")|(m["Поступление на места в рамках особой квоты для лиц, имеющих особое право"] == "+"), "Quota", "No quota")
    m.drop(["Поступление на места по целевой квоте", "Поступление на места в рамках особой квоты для лиц, имеющих особое право", "Право поступления без вступительных испытаний", 'Возврат документов', 'Заявление о согласии на зачисление', "№ п/п", "Бюджетные места", "Платные места", 'Сумма конкурсных баллов'], axis = 1, inplace = True)
    m = pd.melt(m, id_vars=['Образовательная программа', 'Quota'], value_vars=['История ЕГЭ','История ЕГЭ', 'Математика ЕГЭ', 'Биология ЕГЭ', 'Химия','Обществознание ЕГЭ', 'Творческий конкурс Дизайн', 'Физика','География', 'Информатика', 'Литература', 'Русский язык ЕГЭ','Иностранный язык'])
    m.value[m.value == ""] = 0
    m["value"] = m.value.astype(float)
    n = pd.pivot_table(m, values='value', index=['Образовательная программа', 'Quota'],columns = ['variable'], aggfunc=np.mean)
    return (n)
    n.to_excel('D:/VUZD/PythonBD/Example5.xlsx', na_rep='')



def right_program_breakdown():
    m = students[['№ п/п','Заявление о согласии на зачисление',
                  'Право поступления без вступительных испытаний',
                  'Поступление на места в рамках особой квоты для лиц, имеющих особое право',
                  'Поступление на места по целевой квоте','Сумма конкурсных баллов',
                  'Возврат документов','Образовательная программа','Бюджетные места',
                  'Платные места',"История ЕГЭ", "История ЕГЭ",	"Математика ЕГЭ",
                  "Биология ЕГЭ",	"Химия",
                  "Обществознание ЕГЭ",
                  "Творческий конкурс Дизайн",
                  "Физика",	"География",
                  "Информатика", "Литература",
                  "Русский язык ЕГЭ","Иностранный язык"]]
    m = m.loc[m['Заявление о согласии на зачисление'] == '+']
    m = m.loc[m['Поступление на места по целевой квоте'] == '-']
    m = m.loc[m['Поступление на места в рамках особой квоты для лиц, имеющих особое право'] == '-']
    m = m.loc[m['Возврат документов'] == '-']
    m["Right_to_no_exams"] = np.where((m['Право поступления без вступительных испытаний'] != ""), "No_exams", "No_right")
    m.drop(["Поступление на места по целевой квоте",
            "Поступление на места в рамках особой квоты для лиц, имеющих особое право",
            "Право поступления без вступительных испытаний",
            'Возврат документов',
            'Заявление о согласии на зачисление',
            "№ п/п",
            "Бюджетные места", 
            "Платные места",
            'Сумма конкурсных баллов'], axis = 1, inplace = True)
    m = pd.melt(m, id_vars=['Образовательная программа', 'Right_to_no_exams'], value_vars=['История ЕГЭ','История ЕГЭ', 'Математика ЕГЭ', 'Биология ЕГЭ', 'Химия','Обществознание ЕГЭ', 'Творческий конкурс Дизайн', 'Физика','География', 'Информатика', 'Литература', 'Русский язык ЕГЭ','Иностранный язык'])
    m.value[m.value == ""] = 0
    m["value"] = m.value.astype(float)
    n = pd.pivot_table(m, values='value', index=['Образовательная программа', 'Right_to_no_exams'],columns = ['variable'], aggfunc=np.mean)
    return(n)
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
    only_me_df.loc[:, "get_budget_place"] = desired_values
    only_me_dict = only_me_df.T.to_dict()
    only_me_dict = list(only_me_dict.values())
    return(only_me_dict)

#!!!!!!!!!!!!!!!!!!!!!!!ТУТ НАЧИНАЕТСЯ ИНТЕРФЕЙС!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def new_window():
    root.title("Window!")
    root.geometry("1300x642+350+150")
    panel.config(image = img2)
    wel.pack_forget()
    but.pack_forget()
    
    left = tk.Frame(panel, bg="green")
    left.pack(side="left")
    
    right = tk.Frame(panel, bg="blue")
    right.pack(side="right")
    
    
    but_get_snils = tk.Button(left, text = "get SNILS by exam results", font = ("Times",14),  background = "white", command = get_snils)
    but_get_snils.pack(side = "top")
    
    but_places = tk.Button(left, text = "Places for education by educating programm", font = ("Times",14),  background = "white", command = places)
    but_places.pack(side = "top")
        
    but_entrant_data = tk.Button(left, text = "Entrant data", font = ("Times",14),  background = "white", command = Entrant_data)
    but_entrant_data.pack(side = "top")
    
    but_quota = tk.Button(left, text = "Comparison with quota", font = ("Times",14),  background = "white",command = quota)
    but_quota.pack(side = "top")
    
    but_right = tk.Button(left, text = "Comparison with right", font = ("Times",14),  background = "white", command = without_exams)
    but_right.pack(side = "top")
    
    but_programs = tk.Button(right, text = "Data Base образовательные программы", font = ("Times",14),  background = "white", command = bd_programs)
    but_programs.pack(side = "top")
    
    but_za = tk.Button(right, text = "Data Base заявления на зачисления", font = ("Times",14),  background = "white", command = bd_za)
    but_za.pack(side = "top")
    
    but_entrants = tk.Button(right, text = "Data Base абитуриенты", font = ("Times",14),  background = "white", command = bd_entr)
    but_entrants.pack(side = "top")
    
def bd_programs():
        window = tk.Toplevel()
        window.geometry("1000x1000+100+100")
        
        table = ttk.Treeview(window, columns = ("Образовательная программа","Проходной балл","Бюджетные места","Платные места"))
        table.column('#0',width=0, stretch="no")
        table.column('Образовательная программа', anchor="center", width=120)
        table.column('Проходной балл', anchor="center", width=120)
        table.column('Бюджетные места', anchor="center", width=120)
        table.column('Платные места', anchor="center", width=120)
        table.heading('#0', text='', anchor="center")
        table.heading('Образовательная программа', text='Образовательная программа', anchor="center")
        table.heading('Проходной балл', text='Проходной балл', anchor="center")
        table.heading('Бюджетные места', text='Бюджетные места', anchor="center")
        table.heading('Платные места', text='Платные места', anchor="center")
        
        table.pack(side = "top")

def bd_za():
        window = tk.Toplevel()
        window.geometry("1700x1000+100+100")
        
        table = ttk.Treeview(window, columns = ("ID","СНИЛС","Согл. на зачисление","Доп. Балл","Сумма баллов",
                                                "Форма обучения","Возврат документов",
                                                "№ абитуриента","Образовательная программа",
                                                "Преимуществ. право"))
        table.column('#0',width=0, stretch="no")
        table.column('ID', anchor="center", width=140)
        table.column('СНИЛС', anchor="center", width=140)
        table.column('Согл. на зачисление', anchor="center", width=140)
        table.column('Доп. Балл', anchor="center", width=140)
        table.column('Сумма баллов', anchor="center", width=140)
        table.column('Форма обучения', anchor="center", width=140)
        table.column('Возврат документов', anchor="center", width=140)
        table.column('№ абитуриента', anchor="center", width=140)
        table.column('Образовательная программа', anchor="center", width=140)
        table.column('Преимуществ. право', anchor="center", width=140)
        table.heading('#0', text='', anchor="center")
        table.heading('ID', text='ID', anchor="center")
        table.heading('СНИЛС', text='СНИЛС', anchor="center")
        table.heading('Согл. на зачисление', text='Согл. на зачисление', anchor="center")
        table.heading('Доп. Балл', text='Доп. Балл', anchor="center")
        table.heading('Сумма баллов', text='Сумма баллов', anchor="center")
        table.heading('Форма обучения', text='Форма обучения', anchor="center")
        table.heading('Возврат документов', text='Возврат документов', anchor="center")
        table.heading('№ абитуриента', text='№ абитуриента', anchor="center")
        table.heading('Образовательная программа', text='Образовательная программа', anchor="center")
        table.heading('Преимуществ. право', text='Преимуществ. право', anchor="center")
        
        table.pack(side = "top")

def bd_entr():
        window = tk.Toplevel()
        window.geometry("1000x1000+100+100")
        
        table = ttk.Treeview(window, columns = ("СНИЛС","Право без испытаний","Особая квота",
                                                "Целевая квота","Предметы ЕГЭ","Общежитие"))
        table.column('#0',width=0, stretch="no")
        table.column('СНИЛС', anchor="center", width=140)
        table.column('Право без испытаний', anchor="center", width=140)
        table.column('Особая квота', anchor="center", width=140)
        table.column('Целевая квота', anchor="center", width=140)
        table.column('Предметы ЕГЭ', anchor="center", width=140)
        table.column('Общежитие', anchor="center", width=140)

        table.heading('#0', text='', anchor="center")
        table.heading('СНИЛС', text='СНИЛС', anchor="center")
        table.heading('Право без испытаний', text='Право без испытаний', anchor="center")
        table.heading('Особая квота', text='Особая квота', anchor="center")
        table.heading('Целевая квота', text='Целевая квота', anchor="center")
        table.heading('Предметы ЕГЭ', text='Предметы ЕГЭ', anchor="center")
        table.heading('Общежитие', text='Общежитие', anchor="center")
        
        table.pack(side = "top")


def get_snils():
    window = tk.Toplevel()
    window.geometry("1000x900+900+100")
    
    left = tk.Frame(window)
    left.pack(side="left")
    
    exam = tk.Entry(left, width = 25, font = ("Times",20))
    exam.insert("0","Enter the name of the exam")
    exam.pack(side = "top")
    
    points = tk.Entry(left, width = 25, font = ("Times",20))
    points.insert("0","Enter the number of points")
    points.pack(side = "top")
    
    big = tk.Checkbutton(left, text='>', font = ("Times",20))
    big.pack(side = "top")
    
    little = tk.Checkbutton(left, text='<', font = ("Times",20))
    little.pack(side = "top")
    
    equally = tk.Checkbutton(left, text='=', font = ("Times",20))
    equally.pack(side = "top")
    
    start = tk.Button(left, text = "Start", font = ("Lucida Handwriting",10),  background = "white")
    start.pack(side = "top")
    
    save = tk.Button(left, text = "Сохранить в excel", font = ("Lucida Handwriting",10),  background = "white")
    save.pack(side = "top")
    
    message = """
    Данная функция показывает людей согласно их баллам ЕГЭ.
    Таким образом можно проанализировать людей
    с необходимым количеством баллов.
    """
    #" "
    subscribe = tk.Label(left, text = message, font = ("Lucida Handwriting",15))
    subscribe.pack(side = "top")
    
    table = ttk.Treeview(window, columns = ("N","SNILS","Exam name"))
    table.column('#0',width=0, stretch="no")
    table.column('N', anchor="center", width=80)
    table.column('SNILS', anchor="center", width=80)
    table.column('Exam name', anchor="center", width=120)
    table.heading('#0', text='', anchor="center")
    table.heading('N', text='N', anchor="center")
    table.heading('SNILS', text='SNILS', anchor="center")
    table.heading('Exam name', text='Exam name', anchor="center")
    
    table.pack(side = "top")
    
    
    
def places():
    window = tk.Toplevel()
    window.geometry("1000x900+900+100")
    
    left = tk.Frame(window)
    left.pack(side="left")
    
    name = tk.Entry(left, width = 40, font = ("Times",20))
    name.insert("0","Enter the name of the education programm or 'all'")
    name.pack(side = "top")
    
    budget = tk.Checkbutton(left, text = "Убрать обр.программы с бюджетными местами", font = ("Times",20))
    budget.pack(side = "top")
    
    paid = tk.Checkbutton(left, text = "Убрать обр.программы с платными местами", font = ("Times",20))
    paid.pack(side = "top")
    
    start = tk.Button(left, text = "Start", font = ("Lucida Handwriting",10),  background = "white")
    start.pack(side = "top")
    
    save = tk.Button(left, text = "Сохранить в excel", font = ("Lucida Handwriting",10),  background = "white")
    save.pack(side = "top")
    
    message = """
    Эта функция позволяет увидеть таблицу 
    доступных образовательных программ 
    и доступных мест для поступления.
    """
    #" "
    subscribe = tk.Label(left, text = message, font = ("Lucida Handwriting",15))
    subscribe.pack(side = "top")
    
    table = ttk.Treeview(window, columns = ("Образовательная программа","Бюджетные места","Платные места"))
    table.column('#0',width=0, stretch="no")
    table.column('Образовательная программа', anchor="center", width=120)
    table.column('Бюджетные места', anchor="center", width=120)
    table.column('Платные места', anchor="center", width=120)
    table.heading('#0', text='', anchor="center")
    table.heading('Образовательная программа', text='Образовательная программа', anchor="center")
    table.heading('Бюджетные места', text='Бюджетные места', anchor="center")
    table.heading('Платные места', text='Платные места', anchor="center")
    
    table.pack(side = "top")





def Entrant_data():
    window = tk.Toplevel()
    window.geometry("1700x900+100+100")
    operator = ''
    
    table = ttk.Treeview(window, columns = ("N","СНИЛС","Без испытаний","Особое право","Целевая квота","Программа","Сумма баллов"))
    table.column('#0',width=0, stretch="no")
    table.column('N', anchor="center", width=100)
    table.column('СНИЛС', anchor="center", width=100)
    table.column('Без испытаний', anchor="center", width=300)
    table.column('Особое право', anchor="center", width=120)
    table.column('Целевая квота', anchor="center", width=120)
    table.column('Программа', anchor="center", width=120)
    table.column('Сумма баллов', anchor="center", width=120)
    table.heading('#0', text='', anchor="center")
    table.heading('N', text='N', anchor="center")
    table.heading('СНИЛС', text='СНИЛС', anchor="center")
    table.heading('Без испытаний', text='Без испытаний', anchor="center")
    table.heading('Особое право', text='Особое право', anchor="center")
    table.heading('Целевая квота', text='Целевая квота', anchor="center")
    table.heading('Программа', text='Программа', anchor="center")
    table.heading('Сумма баллов', text='Сумма баллов', anchor="center")
    table.pack(side = "right", fill = "both", expand=True)
    

    
    def entrant_data_create_table():
        table.delete(*table.get_children())
        operator = ''
        if little_var.get() == True:
            operator = operator + '<'
        if big_var.get() == True:
            operator = operator + '>'
        if equally_var.get() == True:
            operator = operator + '='
        m = entrant_data(without_exam_var.get(), special_q_var.get(), target_q_var.get(), ed_progaram_var.get(), points_var.get(), operator)
        x = 0
        for i in m.iterrows():
            rowLabels = m.index.tolist()
            table.insert('', x, text=rowLabels[x], values=m.iloc[x,:].tolist())
            x+=1
        

    left = tk.Frame(window)
    left.pack(side="left")
    
    without_exam_var = tk.StringVar()
    without_exam_var.set('')
    right = tk.Radiobutton(left,
                           text = "Убрать абитуриентов с правом без экзаменов",
                           font = ("Times",20), variable=without_exam_var,
                           value='0')
    right.pack(side = "top")
    no_right = tk.Radiobutton(left, 
                              text = "Убрать абитуриентов без права без экзаменов",
                              font = ("Times",20),
                              variable=without_exam_var,
                              value='1')
    no_right.pack(side = "top")
    
    special_q_var = tk.StringVar()
    special_q_var.set('')
    special = tk.Radiobutton(left,
                             text = "Убрать абитуриентов с особой квотой",
                             font = ("Times",20),
                             variable=special_q_var,
                             value='0')
    special.pack(side = "top")
    no_special = tk.Radiobutton(left,
                                text = "Убрать абитуриентов без особой квоты",
                                font = ("Times",20),
                                variable=special_q_var,
                                value='1')
    no_special.pack(side = "top")
    
    target_q_var = tk.StringVar()
    target_q_var.set('')
    target = tk.Radiobutton(left,
                            text = "Убрать абитуриентов с целевой квотой",
                            font = ("Times",20),
                            variable=target_q_var,
                            value='0')
    target.pack(side = "top")
    
    no_target = tk.Radiobutton(left,
                               text = "Убрать абитуриентов без целевой квоты",
                               font = ("Times",20),
                               variable=target_q_var,
                               value='1')
    no_target.pack(side = "top")
    
    ed_progaram_var = tk.StringVar()
    ed_progaram_var.set("Enter the name of the education programm")
    name = tk.Entry(left, width = 35, font = ("Times",20), textvariable = ed_progaram_var)
    name.pack(side = "top")
    
    points_var = tk.StringVar()
    points_var.set("Enter the number of points")
    points_entry = tk.Entry(left, width = 25, font = ("Times",20), textvariable = points_var)
    points_entry.pack(side = "top")
    
    big_var = tk.BooleanVar()
    big_var.set(False)
    big = tk.Checkbutton(left, text='>',
                         font = ("Times",20),
                         variable = big_var,
                         onvalue = True,
                         offvalue = False)
    big.pack(side = "top")
    
    little_var = tk.BooleanVar()
    little_var.set(False)
    little = tk.Checkbutton(left, 
                            text='<', 
                            font = ("Times",20),
                            variable = little_var,
                            onvalue = True,
                            offvalue = False)
    little.pack(side = "top")
    
    equally_var = tk.BooleanVar()
    equally_var.set(False)
    equally = tk.Checkbutton(left, 
                             text='=', 
                             font = ("Times",20),
                             variable = equally_var,
                             onvalue = True,
                             offvalue = False)
    equally.pack(side = "top")
    
    def clear_input():
        without_exam_var.set('')
        special_q_var.set('')
        target_q_var.set('')
    
    clear = tk.Button(left, text = "Очистить выбор", font = ("Times",10),  background = "white", command = clear_input)
    clear.pack(side = "top")
    
    save = tk.Button(left, text = "Сохранить в excel", font = ("Times",10),  background = "white")
    save.pack(side = "top")
    
    start = tk.Button(left, text = "Start", font = ("Times",10),  background = "white", command = entrant_data_create_table)
    start.pack(side = "top")
    
    message = """
    Функция позвляет
    получить данные об абитуриентах
    с определённой образовательной программы.
    """
    #" "
    subscribe = tk.Label(left, text = message, font = ("Lucida Handwriting",15))
    subscribe.pack(side = "top")
    

    


def quota():
    window = tk.Toplevel()
    window.geometry("2000x900+0+100")
    
    left = tk.Frame(window)
    left.pack(side="left")
    
    save = tk.Button(left, text = "Сохранить в excel", font = ("Lucida Handwriting",10),  background = "white")
    save.pack(side = "top")
    
    message = """
    Данная функция позволяет пользователю 
    сравнить средний балл абитуриентов,
    проходящих по квоте, и абитуриентов без квоты.
    Причём рассматриваются только те абитуриенты, 
    которые подали согласие на зачисление 
    и не вернули документы.
    (По идее, количество с толбцов увеличится.
     Будет весь список предметов ЕГЭ.)
    """
    #" "
    subscribe = tk.Label(left, text = message, font = ("Lucida Handwriting",15))
    subscribe.pack(side = "top")
    
    table = ttk.Treeview(window, columns = ("Программа","Есть квота","Без квоты","Биология"))
    table.column('#0',width=0, stretch="no")
    table.column('Программа', anchor="center", width=80)
    table.column('Есть квота', anchor="center", width=80)
    table.column('Без квоты', anchor="center", width=80)
    table.column('Биология', anchor="center", width=120)
    table.heading('#0', text='', anchor="center")
    table.heading('Программа', text='Программа', anchor="center")
    table.heading('Есть квота', text='Есть квота', anchor="center")
    table.heading('Без квоты', text='Без квоты', anchor="center")
    table.heading('Биология', text='Биология', anchor="center")

    table.pack(side = "left")

def without_exams():
    window = tk.Toplevel()
    window.geometry("2000x900+0+100")
    
    left = tk.Frame(window)
    left.pack(side="left")
    
    save = tk.Button(left, text = "Сохранить в excel", font = ("Lucida Handwriting",10),  background = "white")
    save.pack(side = "top")
    
    message = """
    Данная функция позволяет пользователю 
    сравнить средний балл абитуриентов,
    проходящих без вступительных испытаний, 
    и абитуриентов без такого права.
    Причём рассматриваются только те абитуриенты, 
    которые подали согласие на зачисление 
    и не вернули документы.
    (По идее, количество столбцов увеличится.
     Будет весь список предметов ЕГЭ.)
    """
    #" "
    subscribe = tk.Label(left, text = message, font = ("Lucida Handwriting",15))
    subscribe.pack(side = "top")
    
    table = ttk.Treeview(window, columns = ("Программа","Без экзаменов","С экзаменами","Биология"))
    table.column('#0',width=0, stretch="no")
    table.column('Программа', anchor="center", width=80)
    table.column('Без экзаменов', anchor="center", width=80)
    table.column('С экзаменами', anchor="center", width=80)
    table.column('Биология', anchor="center", width=120)
    table.heading('#0', text='', anchor="center")
    table.heading('Программа', text='Программа', anchor="center")
    table.heading('Без экзаменов', text='Без экзаменов', anchor="center")
    table.heading('С экзаменами', text='С экзаменами', anchor="center")
    table.heading('Биология', text='Биология', anchor="center")

    table.pack(side = "left")



root = tk.Tk()

root.title("Welcome!")
root.geometry("428x867+700+100")
#root.wm_attributes('-transparentcolor', root['background'])

path = "IMG_20220509_170259.jpg"
img = Image.open(path)
img = img.resize((428, 867), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)


path2 = "IMG_20220509_170243.jpg"
img2 = Image.open(path2)
img2 = img2.resize((1300, 642), Image.ANTIALIAS)
img2 = ImageTk.PhotoImage(img2)

panel = tk.Label(root, image = img, cursor = "star")
panel.pack(side = "bottom", fill = "both", expand = "yes")


wel = tk.Label(panel, text = "Welcome!", background = "white", font = ("Lucida Handwriting",40), foreground = "#5194ed")
wel.pack()


but = tk.Button(panel, text = "Start", font = ("Lucida Handwriting",40),  background = "white", foreground = "#57612a", command = new_window)
but.pack(side = "bottom")


root.mainloop()







