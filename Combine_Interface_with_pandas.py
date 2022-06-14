import matplotlib.figure
import matplotlib.pyplot as plt

import os
from os import listdir, makedirs, path
import pandas as pd
import numpy as np

import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk
from work.library.telegram_bot import parse_website_link
bot_or_pril = True


def To_Bot(SNILS):
    students = pd.read_excel(f'{os.getcwd()}\\students.xlsx')
    all_students_df = students[["№ п/п", "СНИЛС", "Право поступления без вступительных испытаний",
                                "Поступление на места в рамках особой квоты для лиц, имеющих особое право",
                                "Поступление на места по целевой квоте", "Образовательная программа",
                                "Сумма конкурсных баллов", "Заявление о согласии на зачисление", "Бюджетные места"]]
    only_me_df = all_students_df.loc[all_students_df["СНИЛС"] == SNILS]
    desired_values = []
    for program_name, budget_places in zip(only_me_df["Образовательная программа"].tolist(),
                                           only_me_df["Бюджетные места"].tolist()):
        me_in_this_program = all_students_df[
            (all_students_df["Образовательная программа"] == program_name) & (all_students_df["СНИЛС"] == SNILS)]
        if me_in_this_program["Заявление о согласии на зачисление"].values[0] == "-":
            desired_values.append("-")
        else:
            one_prog_students_df = all_students_df[(all_students_df["Образовательная программа"] == program_name)]
            agreed_one_prog_students_df = one_prog_students_df[
                one_prog_students_df["Заявление о согласии на зачисление"] == "+"]
            agreed_one_prog_students_df.reset_index(inplace=True, drop=True)
            my_number = agreed_one_prog_students_df[agreed_one_prog_students_df["СНИЛС"] == SNILS].index[0]
            if int(budget_places) - int(my_number) >= 0:
                desired_values.append("+")
            else:
                desired_values.append("-")
    only_me_df.loc[:, "get_budget_place"] = desired_values
    only_me_dict = only_me_df.T.to_dict()
    only_me_dict = list(only_me_dict.values())
    return (only_me_dict)


def start_menu():
    global bot_or_pril
    preview_window = tk.Tk()
    preview_window.title("Начало.")
    preview_window.geometry("800x400+600+100")

    def pril():
        global bot_or_pril
        bot_or_pril = True
        preview_window.destroy()


    def bot():
        global bot_or_pril
        bot_or_pril = False
        preview_window.destroy()


    but_bot = tk.Button(preview_window, text="Использовать телеграм-бота", font=("Times", 20), background="white",
                        command=bot)
    but_bot.pack(side="top")

    but_pril = tk.Button(preview_window, text="Использовать приложение", font=("Times", 20), background="white",
                         command=pril)
    but_pril.pack(side="top")

    message = """
    Ваше высочество, вам предстоит выбрать
    в каком формате вы хотите работать с данным ПО.
    Если вам требуются общая статистика и анализ,
    то используйте приложение на компьютере.
    Если вы хотите мобильно узнать свою стаистику,
    то выберите телеграм-бота.
    """
    lab = tk.Label(preview_window, text=message, font=("Times", 20))
    lab.pack(side="bottom")

    preview_window.mainloop()


def info_telegram_bot():
    bot_window = tk.Tk()
    bot_window.geometry("1700x900+100+50")
    bot_window.title("бот")
    lab = tk.Label(bot_window, text="@ParserstatsHSEbot", font=("Times", 50), fg='blue')
    lab.pack(side="top")
    path4 = "telega.png"
    img4 = Image.open(path4)
    img4 = img4.resize((700, 550), Image.Resampling.LANCZOS)
    img4 = ImageTk.PhotoImage(img4)
    panelka = tk.Label(bot_window, image=img4, cursor="pirate")
    panelka.pack(side="top", fill="both", expand="yes")

    message = """
    Ваше высочество, перед вами окно телеграм-бота.
    С помощью этого тэга вы можете ему написать.
    Просьба не закрывать данное окно,
    пока используете телеграмм-бота.
    Спасибо.
    """
    lab = tk.Label(bot_window, text=message, font=("Times", 30))
    lab.pack(side="bottom")
    bot_window.mainloop()


def run_app():
    def get_data(my_path):
        """
        :param my_path: путь к папке стаблицами
        :return: таблица с данными, собранными из всех таблиц
        """
        new_my_path = my_path + "\csv/"
        if not os.path.exists(my_path + "/csv"):
            makedirs(my_path + "/csv")
        for name in listdir(my_path):
            if name == "csv":
                pass
            else:
                buffer = pd.read_excel(f"{my_path}/" + name)
                buffer.to_csv(f"{new_my_path}" + name + ".csv", encoding="cp1251", sep=';', index=False)
        students = pd.DataFrame()
        for name in listdir(new_my_path):
            students = students.append(func(new_my_path, name))
        return students


    # Эта функция достаёт данные
    def func(new_my_path, name):
        """
        :param new_my_path: путь в директории к файлам csv
        :param name: название образовательной программы
        :return: таблица с необходимыми данными
        """
        need_path = new_my_path + name
        # Достаём основную таблицу из файла CSV
        students = np.loadtxt(f"{need_path}",
                              delimiter=';',
                              skiprows=15,
                              encoding="cp1251",
                              dtype='O')
        # Достаём название образовательной программы
        text_mas = np.loadtxt(f"{need_path}",
                              delimiter=';',
                              skiprows=2,
                              encoding="cp1251",
                              max_rows=1,
                              dtype='O')
        napravlenie = str(text_mas)[29:-2]

        # print(Napravlenie)
        # Достаём количество бюджетных мест
        text_mas = np.loadtxt(f"{need_path}",
                              delimiter=';',
                              skiprows=7,
                              encoding="cp1251",
                              max_rows=1,
                              dtype='O')
        budget = int(text_mas[0][27:])
        # Достаём количество платных мест
        text_mas = np.loadtxt(f"{need_path}",
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
        array = np.array("Образовательная программа")
        for i in range(num_of_stud, 1, -1):
            array = np.append(array, napravlenie)
        students = np.c_[students, array]
        array = np.array("Бюджетные места")
        for i in range(num_of_stud, 1, -1):
            array = np.append(array, budget)
        students = np.c_[students, array]
        array = np.array("Платные места")
        for i in range(num_of_stud, 1, -1):
            array = np.append(array, platno)
        students = np.c_[students, array]
        # Запиливаем пандас датафрейм и название столбцов
        students = pd.DataFrame(students[1:, ], columns=students[0,])
        return students


    start_window = tk.Tk()
    start_window.title("Начало.")
    start_window.geometry("800x200+600+300")

    my_path_var = tk.StringVar()
    my_path_var.set("Введите путь к папке с файлами xlsx")


    def get_data_from_path():
        global students
        students = get_data(my_path_var.get())
        start_window.destroy()


    my_path_entry = tk.Entry(start_window, width=40, font=("Times", 20), textvariable=my_path_var)
    my_path_entry.pack(side="top")

    but_path = tk.Button(start_window, text="Запустить", font=("Times", 20), background="white",
                         command=get_data_from_path)
    but_path.pack(side="top")

    link_var = tk.StringVar()
    link_var.set("Или введите ссылку на таблицу")



    def get_link_from_user():
        global students
        try:
            parse_website_link(link_var.get())
            students = pd.read_excel(f'{os.getcwd()}\\work\\library\\students.xlsx')
            students = students.rename(columns={'Русский язык ЕГЭ': 'Русский язык',
                                                'История ЕГЭ': 'История',
                                                'Математика ЕГЭ': 'Математика',
                                                'Биология ЕГЭ': 'Биология',
                                                'Обществознание ЕГЭ': 'Обществознание'})
            start_window.destroy()
        except:
            link_var.set("Некорректная ссылка")

    but_link = tk.Button(start_window, text="Запустить", font=("Times", 20), background="white",
                         command=get_link_from_user)
    but_link.pack(side="bottom")

    link_entry = tk.Entry(start_window, width=40, font=("Times", 20), textvariable=link_var, fg = 'blue')
    link_entry.pack(side="bottom")

    start_window.mainloop()

    # А здесь я начинаю искать нужные мне данные



    def Obr_program_bd():
        n = students[
            ["Заявление о согласии на зачисление", "Возврат документов", "Образовательная программа", "Бюджетные места",
             "Платные места", "Сумма конкурсных баллов"]]
        n = n[n["Заявление о согласии на зачисление"] == "+"]
        n = n[n["Возврат документов"] == "-"]
        n['num'] = n.groupby("Образовательная программа").cumcount()
        n = n[n["Бюджетные места"].astype(int) == n["num"]]
        m = n[["Образовательная программа", "Бюджетные места", "Платные места", "Сумма конкурсных баллов"]]
        m = m.rename(columns={'Сумма конкурсных баллов': 'Проходной балл'})
        m.loc[m["Бюджетные места"].astype(int) == 0, "Проходной балл"] = 0
        m.reset_index(inplace=True, drop=True)
        return m


    def zayavlenie_zachislenie():
        m = students[["СНИЛС",
                      "Заявление о согласии на зачисление",
                      "Балл за индивидуальные достижения",
                      "Сумма конкурсных баллов",
                      "Форма обучения",
                      "Возврат документов",
                      "№ п/п",
                      "Образовательная программа"]]
        return (m)


    def entrant_data_base():
        m = students[["СНИЛС",
                      "Право поступления без вступительных испытаний",
                      "Поступление на места в рамках особой квоты для лиц, имеющих особое право",
                      "Поступление на места по целевой квоте",
                      'Литература',
                      'Русский язык',
                      'Иностранный язык',
                      'История',
                      'Математика',
                      'Биология',
                      'Химия',
                      'Обществознание',
                      'Творческий конкурс Дизайн',
                      'Физика',
                      'География',
                      'Информатика',
                      'Творческий конкурс Медиа',
                      'Творческий конкурс Мода',
                      'Творческий конкурс I этап',
                      "Требуется общежитие на время обучения",
                      ]]
        return m


    def entrant_data(without_exam, special_q, target_q, ed_progaram, points, operator):
        m = students[["№ п/п", "СНИЛС",
                      "Право поступления без вступительных испытаний",
                      "Поступление на места в рамках особой квоты для лиц, имеющих особое право",
                      "Поступление на места по целевой квоте", "Образовательная программа",
                      "Сумма конкурсных баллов"]]
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
        return m


    def Get_SNILS_by_exam(exam, points, operator):
        if exam in students:
            m = students[["СНИЛС", exam, "Сумма конкурсных баллов"]]
            counts = {"< " + str(points): 0, "= " + str(points): 0, "> " + str(points): 0}
            m = m[~m[exam].isnull()]
            m = m[m[exam] != ""]
            m.loc[m[exam] == "", exam] = 0
            m.loc[:, exam] = m[exam].astype(int)
            figure = matplotlib.figure.Figure(figsize=(10, 10), dpi=100)
            plot = figure.add_subplot(212)
            plot.boxplot(m[[exam]], notch=True, showmeans=True, whis=1.5, vert=False, showfliers=False)
            try:
                points = int(points)
            except ValueError:
                error_of_int = True
            else:
                error_of_int = False
            if error_of_int == False:
                for score in m[exam]:
                    if score < points:
                        counts["< " + str(points)] += 1
                    elif score == points:
                        counts["= " + str(points)] += 1
                    else:
                        counts["> " + str(points)] += 1
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
                elif operator == '<>':
                    m = m[m[exam] != points]
                elif operator == '<>=':
                    pass
                else:
                    m = m[m[exam] > points]
            m.reset_index(inplace=True, drop=True)
            plot1 = figure.add_subplot(211)
            plot1.pie(counts.values(), labels=counts.keys())
            m = m.sort_values(exam)
            return m, figure
        else:
            data = {"СНИЛС": ["Нет"],
                    exam: ["0"],
                    "Сумма конкурсных баллов": ["0"]}
            m = pd.DataFrame(data)
            n = m
            m.reset_index(inplace=True, drop=True)
            m = m.set_index("СНИЛС")
            m.loc[:, exam] = m[exam].astype(int)
            m.loc[:, "Сумма конкурсных баллов"] = m["Сумма конкурсных баллов"].astype(int)
            m.reset_index(inplace=True, drop=True)
            bar_graph = m.plot(figsize=(26, 25), kind="bar")
            figure = bar_graph.get_figure()
            return n, figure


    def Places_for_education(name, budget, paid):
        m = students[["Образовательная программа", "Бюджетные места", "Платные места"]]
        m = m.drop_duplicates(subset='Образовательная программа', keep='first')
        m.reset_index(inplace=True, drop=True)
        name = '"' + name + '"'
        if name in m["Образовательная программа"].values:
            m = m[m["Образовательная программа"] == name]
        else:
            pass
        if budget == True:
            m = m[m["Бюджетные места"] == "0"]
        if paid == True:
            m = m[m["Платные места"] == "0"]
        n = m
        isempty = n.empty
        if isempty == False:
            m.reset_index(inplace=True, drop=True)
            m = m.set_index("Образовательная программа")
            m.loc[:, "Бюджетные места"] = m["Бюджетные места"].astype(int)
            m.loc[:, "Платные места"] = m["Платные места"].astype(int)
            bar_graph = m.plot(figsize=(26, 25), kind="bar")
            figure = bar_graph.get_figure()
        else:
            data = {"Образовательная программа": ["Нет"],
                    "Бюджетные места": ["0"],
                    "Платные места": ["0"]}
            m = pd.DataFrame(data)
            n = m
            m.reset_index(inplace=True, drop=True)
            m = m.set_index("Образовательная программа")
            m.loc[:, "Бюджетные места"] = m["Бюджетные места"].astype(int)
            m.loc[:, "Платные места"] = m["Платные места"].astype(int)
            bar_graph = m.plot(figsize=(26, 25), kind="bar")
            figure = bar_graph.get_figure()
        return n, figure


    def quota_program_breakdown():
        m = students[['№ п/п', 'Заявление о согласии на зачисление',
                      'Право поступления без вступительных испытаний',
                      'Поступление на места в рамках особой квоты для лиц, имеющих особое право',
                      'Поступление на места по целевой квоте',
                      'Сумма конкурсных баллов', 'Возврат документов',
                      'Образовательная программа', 'Бюджетные места',
                      'Платные места',
                      'Литература',
                      'Русский язык',
                      'Иностранный язык',
                      'История',
                      'Математика',
                      'Биология',
                      'Химия',
                      'Обществознание',
                      'Творческий конкурс Дизайн',
                      'Физика',
                      'География',
                      'Информатика',
                      'Творческий конкурс Медиа',
                      'Творческий конкурс Мода',
                      'Творческий конкурс I этап']]

        m = m.loc[m['Заявление о согласии на зачисление'] == '+']
        m = m.loc[m['Право поступления без вступительных испытаний'] == '']
        m = m.loc[m['Возврат документов'] == '-']
        m["Quota"] = np.where((m["Поступление на места по целевой квоте"] == "+") | (
                    m["Поступление на места в рамках особой квоты для лиц, имеющих особое право"] == "+"), "Quota",
                              "No quota")
        m.drop(["Поступление на места по целевой квоте",
                "Поступление на места в рамках особой квоты для лиц, имеющих особое право",
                "Право поступления без вступительных испытаний", 'Возврат документов',
                'Заявление о согласии на зачисление', "№ п/п", "Бюджетные места", "Платные места",
                'Сумма конкурсных баллов'], axis=1, inplace=True)
        m = pd.melt(m, id_vars=['Образовательная программа', 'Quota'], value_vars=['Литература',
                                                                                   'Русский язык',
                                                                                   'Иностранный язык',
                                                                                   'История',
                                                                                   'Математика',
                                                                                   'Биология',
                                                                                   'Химия',
                                                                                   'Обществознание',
                                                                                   'Творческий конкурс Дизайн',
                                                                                   'Физика',
                                                                                   'География',
                                                                                   'Информатика',
                                                                                   'Творческий конкурс Медиа',
                                                                                   'Творческий конкурс Мода',
                                                                                   'Творческий конкурс I этап'])
        m.value[m.value == ""] = 0
        m["value"] = m.value.astype(float)
        n = pd.pivot_table(m, values='value', index=['Образовательная программа', 'Quota'], columns=['variable'],
                           aggfunc=np.mean)
        n.to_excel('./quota_program_breakdown.xlsx', na_rep='')


    def quota_program_breakdown_for_treeview():
        m = students[['№ п/п', 'Заявление о согласии на зачисление',
                      'Право поступления без вступительных испытаний',
                      'Поступление на места в рамках особой квоты для лиц, имеющих особое право',
                      'Поступление на места по целевой квоте',
                      'Сумма конкурсных баллов', 'Возврат документов',
                      'Образовательная программа', 'Бюджетные места',
                      'Платные места',
                      'Литература',
                      'Русский язык',
                      'Иностранный язык',
                      'История',
                      'Математика',
                      'Биология',
                      'Химия',
                      'Обществознание',
                      'Творческий конкурс Дизайн',
                      'Физика',
                      'География',
                      'Информатика',
                      'Творческий конкурс Медиа',
                      'Творческий конкурс Мода',
                      'Творческий конкурс I этап']]
        m = m.loc[m['Заявление о согласии на зачисление'] == '+']
        m = m.loc[m['Право поступления без вступительных испытаний'] == '']
        m = m.loc[m['Возврат документов'] == '-']
        m["Quota"] = np.where((m["Поступление на места по целевой квоте"] == "+") | (
                    m["Поступление на места в рамках особой квоты для лиц, имеющих особое право"] == "+"), "Quota",
                              "No quota")
        m.drop(["Поступление на места по целевой квоте",
                "Поступление на места в рамках особой квоты для лиц, имеющих особое право",
                "Право поступления без вступительных испытаний", 'Возврат документов',
                'Заявление о согласии на зачисление', "№ п/п", "Бюджетные места", "Платные места",
                'Сумма конкурсных баллов'], axis=1, inplace=True)
        m = pd.melt(m, id_vars=['Образовательная программа', 'Quota'], value_vars=['Литература',
                                                                                   'Русский язык',
                                                                                   'Иностранный язык',
                                                                                   'История',
                                                                                   'Математика',
                                                                                   'Биология',
                                                                                   'Химия',
                                                                                   'Обществознание',
                                                                                   'Творческий конкурс Дизайн',
                                                                                   'Физика',
                                                                                   'География',
                                                                                   'Информатика',
                                                                                   'Творческий конкурс Медиа',
                                                                                   'Творческий конкурс Мода',
                                                                                   'Творческий конкурс I этап'])
        m.value[m.value == ""] = 0
        m["value"] = m.value.astype(float)
        n = pd.pivot_table(m, values='value', index=['Образовательная программа', 'Quota'], columns=['variable'],
                           aggfunc=np.mean).reset_index()
        return (n)


    def right_program_breakdown():
        m = students[['№ п/п', 'Заявление о согласии на зачисление',
                      'Право поступления без вступительных испытаний',
                      'Поступление на места в рамках особой квоты для лиц, имеющих особое право',
                      'Поступление на места по целевой квоте', 'Сумма конкурсных баллов',
                      'Возврат документов', 'Образовательная программа', 'Бюджетные места',
                      'Платные места',
                      'Литература',
                      'Русский язык',
                      'Иностранный язык',
                      'История',
                      'Математика',
                      'Биология',
                      'Химия',
                      'Обществознание',
                      'Творческий конкурс Дизайн',
                      'Физика',
                      'География',
                      'Информатика',
                      'Творческий конкурс Медиа',
                      'Творческий конкурс Мода',
                      'Творческий конкурс I этап']]
        m = m.loc[m['Заявление о согласии на зачисление'] == '+']
        m = m.loc[m['Поступление на места по целевой квоте'] == '-']
        m = m.loc[m['Поступление на места в рамках особой квоты для лиц, имеющих особое право'] == '-']
        m = m.loc[m['Возврат документов'] == '-']
        m["Right_to_no_exams"] = np.where((m['Право поступления без вступительных испытаний'] != ""), "No_exams",
                                          "No_right")
        m.drop(["Поступление на места по целевой квоте",
                "Поступление на места в рамках особой квоты для лиц, имеющих особое право",
                "Право поступления без вступительных испытаний",
                'Возврат документов',
                'Заявление о согласии на зачисление',
                "№ п/п",
                "Бюджетные места",
                "Платные места",
                'Сумма конкурсных баллов'], axis=1, inplace=True)
        m = pd.melt(m, id_vars=['Образовательная программа', 'Right_to_no_exams'], value_vars=['Литература',
                                                                                               'Русский язык',
                                                                                               'Иностранный язык',
                                                                                               'История',
                                                                                               'Математика',
                                                                                               'Биология',
                                                                                               'Химия',
                                                                                               'Обществознание',
                                                                                               'Творческий конкурс Дизайн',
                                                                                               'Физика',
                                                                                               'География',
                                                                                               'Информатика',
                                                                                               'Творческий конкурс Медиа',
                                                                                               'Творческий конкурс Мода',
                                                                                               'Творческий конкурс I этап'])
        m.value[m.value == ""] = 0
        m["value"] = m.value.astype(float)
        n = pd.pivot_table(m, values='value', index=['Образовательная программа', 'Right_to_no_exams'],
                           columns=['variable'], aggfunc=np.mean)
        n.to_excel('./right_program_breakdown.xlsx', na_rep='')


    def right_program_breakdown_for_treeview():
        m = students[['№ п/п', 'Заявление о согласии на зачисление',
                      'Право поступления без вступительных испытаний',
                      'Поступление на места в рамках особой квоты для лиц, имеющих особое право',
                      'Поступление на места по целевой квоте', 'Сумма конкурсных баллов',
                      'Возврат документов', 'Образовательная программа', 'Бюджетные места',
                      'Платные места',
                      'Литература',
                      'Русский язык',
                      'Иностранный язык',
                      'История',
                      'Математика',
                      'Биология',
                      'Химия',
                      'Обществознание',
                      'Творческий конкурс Дизайн',
                      'Физика',
                      'География',
                      'Информатика',
                      'Творческий конкурс Медиа',
                      'Творческий конкурс Мода',
                      'Творческий конкурс I этап']]
        m = m.loc[m['Заявление о согласии на зачисление'] == '+']
        m = m.loc[m['Поступление на места по целевой квоте'] == '-']
        m = m.loc[m['Поступление на места в рамках особой квоты для лиц, имеющих особое право'] == '-']
        m = m.loc[m['Возврат документов'] == '-']
        m["Right_to_no_exams"] = np.where((m['Право поступления без вступительных испытаний'] != ""), "No_exams",
                                          "No_right")
        m.drop(["Поступление на места по целевой квоте",
                "Поступление на места в рамках особой квоты для лиц, имеющих особое право",
                "Право поступления без вступительных испытаний",
                'Возврат документов',
                'Заявление о согласии на зачисление',
                "№ п/п",
                "Бюджетные места",
                "Платные места",
                'Сумма конкурсных баллов'], axis=1, inplace=True)
        m = pd.melt(m, id_vars=['Образовательная программа', 'Right_to_no_exams'], value_vars=['Литература',
                                                                                               'Русский язык',
                                                                                               'Иностранный язык',
                                                                                               'История',
                                                                                               'Математика',
                                                                                               'Биология',
                                                                                               'Химия',
                                                                                               'Обществознание',
                                                                                               'Творческий конкурс Дизайн',
                                                                                               'Физика',
                                                                                               'География',
                                                                                               'Информатика',
                                                                                               'Творческий конкурс Медиа',
                                                                                               'Творческий конкурс Мода',
                                                                                               'Творческий конкурс I этап'])
        m.value[m.value == ""] = 0
        m["value"] = m.value.astype(float)
        n = pd.pivot_table(m, values='value', index=['Образовательная программа', 'Right_to_no_exams'],
                           columns=['variable'], aggfunc=np.mean).reset_index()
        return (n)




    def save_file(file, file_name, path):
        """
        :param file: string, переменная, содержащая данные, которые необходимо сохранить
        :param file_name: string, имя для будущего файла. Без расширения
        :param path: string, путь к папке для сохранения файла
        :return: файл в формате .png или .xlsx
        """
        if os.path.isdir(path) == True:
            if isinstance(file, pd.DataFrame):
                file.to_excel(path + "/" + file_name + ".xlsx")
            elif isinstance(file, matplotlib.figure.Figure):
                file.savefig(path + "/" + file_name + ".png")


    # !!!!!!!!!!!!!!!!!!!!!!!ТУТ НАЧИНАЕТСЯ ИНТЕРФЕЙС!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def graph_window(name_graph, path_graph):
        if os.path.isdir(path_graph) == True:
            graph_window = tk.Toplevel()
            graph_window.title(f'{name_graph}')
            graph_window.geometry("1500x1020+0+0")
            pathw = path_graph + "/" + name_graph + ".png"
            img3 = Image.open(pathw)
            img3 = img3.resize((1500, 1000), Image.ANTIALIAS)
            img3 = ImageTk.PhotoImage(img3)
            pan = tk.Label(graph_window, image=img3, cursor="star")
            pan.pack(side="top", fill="both", expand="yes")
            graph_window.mainloop()


    def new_window():
        root.title("Window!")
        root.geometry("1300x642+350+150")
        panel.config(image=img2)
        wel.pack_forget()
        but.pack_forget()

        left = tk.Frame(panel, bg="green")
        left.pack(side="left")

        right = tk.Frame(panel, bg="blue")
        right.pack(side="right")

        but_get_snils = tk.Button(left, text="Статистика баллов ЕГЭ", font=("Times", 14), background="white",
                                  command=get_snils)
        but_get_snils.pack(side="top")

        but_places = tk.Button(left, text="Места в образовательных программах", font=("Times", 14), background="white",
                               command=places)
        but_places.pack(side="top")

        but_entrant_data = tk.Button(left, text="Данные абитуриентов", font=("Times", 14), background="white",
                                     command=Entrant_data)
        but_entrant_data.pack(side="top")

        but_quota = tk.Button(left, text="Сравнение с квотой", font=("Times", 14), background="white", command=quota)
        but_quota.pack(side="top")

        but_right = tk.Button(left, text="Сравнение с правом без экзаменов", font=("Times", 14), background="white",
                              command=without_exams)
        but_right.pack(side="top")

        but_programs = tk.Button(right, text="Data Base образовательные программы", font=("Times", 14),
                                 background="white", command=bd_programs)
        but_programs.pack(side="top")

        but_za = tk.Button(right, text="Data Base заявления на зачисления", font=("Times", 14), background="white",
                           command=bd_za)
        but_za.pack(side="top")

        but_entrants = tk.Button(right, text="Data Base абитуриенты", font=("Times", 14), background="white",
                                 command=bd_entr)
        but_entrants.pack(side="top")


    def bd_programs():
        window = tk.Toplevel()
        window.geometry("1000x1000+100+100")
        style = ttk.Style(window)
        style.theme_use("clam")

        def fixed_map(option):
            return [elm for elm in
                    style.map('Treeview', background="white", fieldbackground="white", foreground="black") if
                    elm[:2] != ('!disabled', '!selected')]

        table = ttk.Treeview(window, columns=(
        "Образовательная программа", "Бюджетные места", "Платные места", "Проходной балл"))
        table.column('#0', width=0, stretch="no")
        table.column('Образовательная программа', anchor="center", width=120)
        table.column('Бюджетные места', anchor="center", width=120)
        table.column('Платные места', anchor="center", width=120)
        table.column('Проходной балл', anchor="center", width=120)
        table.heading('#0', text='', anchor="center")
        table.heading('Образовательная программа', text='Образовательная программа', anchor="center")
        table.heading('Проходной балл', text='Проходной балл', anchor="center")
        table.heading('Бюджетные места', text='Бюджетные места', anchor="center")
        table.heading('Платные места', text='Платные места', anchor="center")
        table.pack(side="top", fill="both", expand=True)
        Obr_program_table = Obr_program_bd()
        x = 0
        for i in Obr_program_table.iterrows():
            rowLabels = Obr_program_table.index.tolist()
            table.insert('', x, text=rowLabels[x], values=Obr_program_table.iloc[x, :].tolist())
            x += 1

        def night_theme():
            window.config(bg="#3E3D45")
            style.map('Treeview', foreground=fixed_map('foreground'),
                      background=fixed_map('background'))
            style.configure("Treeview", background="#3E3D45",
                            fieldbackground="#3E3D45",
                            foreground="#E1DFEE")

        def day_theme():
            window.config(bg="#f0f0f0")
            style.map('Treeview', foreground=fixed_map('foreground'),
                      background=fixed_map('background'))
            style.configure("Treeview", background="white",
                            fieldbackground="white",
                            foreground="black")

        def save_bd_programs():
            Obr_program_table.to_excel('./Data_base_educating_program.xlsx', na_rep='')

        mainmenu = tk.Menu(window, tearoff=0)
        menu1 = tk.Menu(mainmenu, tearoff=0)
        menu1.add_command(label='Сохранить xlsx', command=save_bd_programs)
        menu1.add_command(label='Тёмная тема', command=night_theme)
        menu1.add_command(label='Светлая тема', command=day_theme)
        mainmenu.add_cascade(label="тема", menu=menu1)
        mainmenu.add_command(label="Exit", command=window.destroy)
        window.config(menu=mainmenu)


    def bd_za():
        window = tk.Toplevel()
        window.geometry("2000x900+0+0")
        style = ttk.Style(window)
        style.theme_use("clam")

        def fixed_map(option):
            return [elm for elm in
                    style.map('Treeview', background="white", fieldbackground="white", foreground="black") if
                    elm[:2] != ('!disabled', '!selected')]

        table = ttk.Treeview(window, columns=("СНИЛС", "Согл. на зачисление", "Доп. Балл", "Сумма баллов",
                                              "Форма обучения", "Возврат документов",
                                              "№ абитуриента", "Образовательная программа"))
        table.column('#0', width=0, stretch="no")
        table.column('СНИЛС', anchor="center", width=140)
        table.column('Согл. на зачисление', anchor="center", width=140)
        table.column('Доп. Балл', anchor="center", width=140)
        table.column('Сумма баллов', anchor="center", width=140)
        table.column('Форма обучения', anchor="center", width=140)
        table.column('Возврат документов', anchor="center", width=140)
        table.column('№ абитуриента', anchor="center", width=140)
        table.column('Образовательная программа', anchor="center", width=140)
        table.heading('#0', text='', anchor="center")
        table.heading('СНИЛС', text='СНИЛС', anchor="center")
        table.heading('Согл. на зачисление', text='Согл. на зачисление', anchor="center")
        table.heading('Доп. Балл', text='Доп. Балл', anchor="center")
        table.heading('Сумма баллов', text='Сумма баллов', anchor="center")
        table.heading('Форма обучения', text='Форма обучения', anchor="center")
        table.heading('Возврат документов', text='Возврат документов', anchor="center")
        table.heading('№ абитуриента', text='№ абитуриента', anchor="center")
        table.heading('Образовательная программа', text='Образовательная программа', anchor="center")
        table.pack(side="top", fill="both", expand=True)
        zz = zayavlenie_zachislenie()
        x = 0
        for i in zz.iterrows():
            rowLabels = zz.index.tolist()
            table.insert('', x, text=rowLabels[x], values=zz.iloc[x, :].tolist())
            x += 1

        def night_theme():
            window.config(bg="#3E3D45")
            style.map('Treeview', foreground=fixed_map('foreground'),
                      background=fixed_map('background'))
            style.configure("Treeview", background="#3E3D45",
                            fieldbackground="#3E3D45",
                            foreground="#E1DFEE")

        def day_theme():
            window.config(bg="#f0f0f0")
            style.map('Treeview', foreground=fixed_map('foreground'),
                      background=fixed_map('background'))
            style.configure("Treeview", background="white",
                            fieldbackground="white",
                            foreground="black")

        def save_bd_zz():
            zz.to_excel('./Data_base_zayavlenia.xlsx', na_rep='')

        mainmenu = tk.Menu(window, tearoff=0)
        menu1 = tk.Menu(mainmenu, tearoff=0)
        menu1.add_command(label='Сохранить xlsx', command=save_bd_zz)
        menu1.add_command(label='Тёмная тема', command=night_theme)
        menu1.add_command(label='Светлая тема', command=day_theme)
        mainmenu.add_cascade(label="тема", menu=menu1)
        mainmenu.add_command(label="Exit", command=window.destroy)
        window.config(menu=mainmenu)


    def bd_entr():
        window = tk.Toplevel()
        window.geometry("2000x900+0+0")
        style = ttk.Style(window)
        style.theme_use("clam")

        def fixed_map(option):
            return [elm for elm in
                    style.map('Treeview', background="white", fieldbackground="white", foreground="black") if
                    elm[:2] != ('!disabled', '!selected')]

        table = ttk.Treeview(window, columns=("СНИЛС",
                                              "Право без испытаний",
                                              "Особая квота",
                                              "Целевая квота",
                                              'Литература',
                                              'Русский язык',
                                              'Иностранный язык',
                                              'История',
                                              'Математика',
                                              'Биология',
                                              'Химия',
                                              'Обществознание',
                                              'Творческий конкурс Дизайн',
                                              'Физика',
                                              'География',
                                              'Информатика',
                                              'Творческий конкурс Медиа',
                                              'Творческий конкурс Мода',
                                              'Творческий конкурс I этап',
                                              "Общежитие"))
        table.column('#0', width=0, stretch="no")
        table.column('СНИЛС', anchor="center", width=140)
        table.column('Право без испытаний', anchor="center", width=140)
        table.column('Особая квота', anchor="center", width=140)
        table.column('Литература', anchor="center", width=80)
        table.column('Русский язык', anchor="center", width=80)
        table.column('Иностранный язык', anchor="center", width=80)
        table.column('История', anchor="center", width=80)
        table.column('Математика', anchor="center", width=80)
        table.column('Биология', anchor="center", width=80)
        table.column('Химия', anchor="center", width=80)
        table.column('Обществознание', anchor="center", width=80)
        table.column('Творческий конкурс Дизайн', anchor="center", width=80)
        table.column('Физика', anchor="center", width=80)
        table.column('География', anchor="center", width=80)
        table.column('Информатика', anchor="center", width=80)
        table.column('Творческий конкурс Медиа', anchor="center", width=80)
        table.column('Творческий конкурс Мода', anchor="center", width=80)
        table.column('Творческий конкурс I этап', anchor="center", width=80)
        table.column('Общежитие', anchor="center", width=140)
        table.heading('#0', text='', anchor="center")
        table.heading('СНИЛС', text='СНИЛС', anchor="center")
        table.heading('Право без испытаний', text='Право без испытаний', anchor="center")
        table.heading('Особая квота', text='Особая квота', anchor="center")
        table.heading('Целевая квота', text='Целевая квота', anchor="center")
        table.heading('Литература', text='Литература', anchor="center")
        table.heading('Русский язык', text='Русский язык', anchor="center")
        table.heading('Иностранный язык', text='Иностранный язык', anchor="center")
        table.heading('История', text='История', anchor="center")
        table.heading('Математика', text='Математика', anchor="center")
        table.heading('Биология', text='Биология', anchor="center")
        table.heading('Химия', text='Химия', anchor="center")
        table.heading('Обществознание', text='Обществознание', anchor="center")
        table.heading('Творческий конкурс Дизайн', text='Творческий конкурс Дизайн', anchor="center")
        table.heading('Физика', text='Физика', anchor="center")
        table.heading('География', text='География', anchor="center")
        table.heading('Информатика', text='Информатика', anchor="center")
        table.heading('Творческий конкурс Медиа', text='Т.к. Медиа', anchor="center")
        table.heading('Творческий конкурс Мода', text='Т.к. Мода', anchor="center")
        table.heading('Творческий конкурс I этап', text='Т.к. I этап', anchor="center")
        table.heading('Общежитие', text='Общежитие', anchor="center")
        table.pack(side="top", fill="both", expand=True)
        entrants = entrant_data_base()
        x = 0
        for i in entrants.iterrows():
            rowLabels = entrants.index.tolist()
            table.insert('', x, text=rowLabels[x], values=entrants.iloc[x, :].tolist())
            x += 1

        def night_theme():
            window.config(bg="#3E3D45")
            style.map('Treeview', foreground=fixed_map('foreground'),
                      background=fixed_map('background'))
            style.configure("Treeview", background="#3E3D45",
                            fieldbackground="#3E3D45",
                            foreground="#E1DFEE")

        def day_theme():
            window.config(bg="#f0f0f0")
            style.map('Treeview', foreground=fixed_map('foreground'),
                      background=fixed_map('background'))
            style.configure("Treeview", background="white",
                            fieldbackground="white",
                            foreground="black")

        def save_bd_entrants():
            entrants.to_excel('./Data_base_entrants.xlsx', na_rep='')

        mainmenu = tk.Menu(window, tearoff=0)
        menu1 = tk.Menu(mainmenu, tearoff=0)
        menu1.add_command(label='Сохранить xlsx', command=save_bd_entrants)
        menu1.add_command(label='Тёмная тема', command=night_theme)
        menu1.add_command(label='Светлая тема', command=day_theme)
        mainmenu.add_cascade(label="тема", menu=menu1)
        mainmenu.add_command(label="Exit", command=window.destroy)
        window.config(menu=mainmenu)
        table.pack(side="top")


    def get_snils():
        window = tk.Toplevel()
        window.geometry("1000x900")
        style = ttk.Style(window)
        style.theme_use("clam")

        def fixed_map(option):
            return [elm for elm in
                    style.map('Treeview', background="white", fieldbackground="white", foreground="black") if
                    elm[:2] != ('!disabled', '!selected')]

        table = ttk.Treeview(window, columns=("SNILS", "Exam name", "points"))
        table.column('#0', width=0, stretch="no")
        table.column('SNILS', anchor="center", width=80)
        table.column('Exam name', anchor="center", width=120)
        table.column('points', anchor="center", width=120)
        table.heading('#0', text='', anchor="center")
        table.heading('SNILS', text='СНИЛС', anchor="center")
        table.heading('Exam name', text='Экзамен', anchor="center")
        table.heading('points', text='Сумма баллов', anchor="center")
        table.pack(side="right", fill="both", expand=True)

        def night_theme():
            window.config(bg="#3E3D45")
            left.config(bg="#3E3D45")
            name.config(bg="#3E3D45", fg="#E1DFEE")
            points_entry.config(bg="#3E3D45", fg="#E1DFEE")
            big.config(bg="#3E3D45", fg="#E1DFEE", selectcolor="#3E3D45")
            little.config(bg="#3E3D45", fg="#E1DFEE", selectcolor="#3E3D45")
            equally.config(bg="#3E3D45", fg="#E1DFEE", selectcolor="#3E3D45")
            clear.config(bg="#3E3D45", fg="#E1DFEE")
            start.config(bg="#3E3D45", fg="#E1DFEE")
            path_xlsx.config(bg="#3E3D45", fg="#E1DFEE")
            name_xlsx.config(bg="#3E3D45", fg="#E1DFEE")
            create_graph.config(bg="#3E3D45", fg="#E1DFEE", selectcolor="#3E3D45")
            path_graph.config(bg="#3E3D45", fg="#E1DFEE")
            name_graph.config(bg="#3E3D45", fg="#E1DFEE")
            save_button.config(bg="#3E3D45", fg="#E1DFEE")
            subscribe.config(bg="#3E3D45", fg="#E1DFEE")
            style.map('Treeview', foreground=fixed_map('foreground'),
                      background=fixed_map('background'))
            style.configure("Treeview", background="#3E3D45",
                            fieldbackground="#3E3D45",
                            foreground="#E1DFEE")

        def day_theme():
            window.config(bg="#f0f0f0")
            left.config(bg="#f0f0f0")
            name.config(bg="white", fg="#000000")
            points_entry.config(bg="white", fg="#000000")
            big.config(bg="#f0f0f0", fg="#000000")
            little.config(bg="#f0f0f0", fg="#000000")
            equally.config(bg="#f0f0f0", fg="#000000")
            clear.config(bg="white", fg="#000000")
            start.config(bg="white", fg="#000000")
            path_xlsx.config(bg="white", fg="#000000")
            name_xlsx.config(bg="white", fg="#000000")
            create_graph.config(bg="#f0f0f0", fg="#000000")
            path_graph.config(bg="white", fg="#000000")
            name_graph.config(bg="white", fg="#000000")
            save_button.config(bg="white", fg="#000000")
            subscribe.config(bg="#f0f0f0", fg="#000000")
            style.map('Treeview', foreground=fixed_map('foreground'),
                      background=fixed_map('background'))
            style.configure("Treeview", background="white",
                            fieldbackground="white",
                            foreground="black")

        def get_snils_create_table():
            table.delete(*table.get_children())
            operator = ''
            if little_var.get() == True:
                operator = operator + '<'
            if big_var.get() == True:
                operator = operator + '>'
            if equally_var.get() == True:
                operator = operator + '='
            m = Get_SNILS_by_exam(exam_var.get(), points_var.get(), operator)
            x = 0
            for i in m[0].iterrows():
                rowLabels = m[0].index.tolist()
                table.insert('', x, text=rowLabels[x], values=m[0].iloc[x, :].tolist())
                x += 1

        def save_get_snils():
            operator = ''
            if little_var.get() == True:
                operator = operator + '<'
            if big_var.get() == True:
                operator = operator + '>'
            if equally_var.get() == True:
                operator = operator + '='
            m = Get_SNILS_by_exam(exam_var.get(), points_var.get(), operator)
            save_file(m[0], name_xlsx_var.get(), path_xlsx_var.get())
            if create_graph_var.get() == True:
                save_file(m[1], name_graph_var.get(), path_graph_var.get())
                graph_window(name_graph_var.get(), path_graph_var.get())

        left = tk.Frame(window)
        left.pack(side="left")

        exam_var = tk.StringVar()
        exam_var.set("Введите название экзамена")

        exam_list = ['Литература',
                     'Русский язык',
                     'Иностранный язык',
                     'История',
                     'Математика',
                     'Биология',
                     'Химия',
                     'Обществознание',
                     'Творческий конкурс Дизайн',
                     'Физика',
                     'География',
                     'Информатика',
                     'Творческий конкурс Медиа',
                     'Творческий конкурс Мода',
                     'Творческий конкурс I этап']

        def lit():
            exam_var.set(exam_list[0])

        def rus():
            exam_var.set(exam_list[1])

        def ino():
            exam_var.set(exam_list[2])

        def his():
            exam_var.set(exam_list[3])

        def math():
            exam_var.set(exam_list[4])

        def bio():
            exam_var.set(exam_list[5])

        def chem():
            exam_var.set(exam_list[6])

        def obsh():
            exam_var.set(exam_list[7])

        def des():
            exam_var.set(exam_list[8])

        def phys():
            exam_var.set(exam_list[9])

        def geo():
            exam_var.set(exam_list[10])

        def info():
            exam_var.set(exam_list[11])

        def Media():
            exam_var.set(exam_list[12])

        def Moda():
            exam_var.set(exam_list[13])

        def I_etap():
            exam_var.set(exam_list[14])

        mainmenu = tk.Menu(window, tearoff=0)
        menu1 = tk.Menu(mainmenu, tearoff=0)
        menu1.add_command(label='Тёмная тема', command=night_theme)
        menu1.add_command(label='Светлая тема', command=day_theme)
        menu_exams = tk.Menu(mainmenu, tearoff=0)
        menu_exams.add_command(label='Литература', command=lit)
        menu_exams.add_command(label='Русский язык', command=rus)
        menu_exams.add_command(label='Иностранный язык', command=ino)
        menu_exams.add_command(label='История', command=his)
        menu_exams.add_command(label='Математика', command=math)
        menu_exams.add_command(label='Биология', command=bio)
        menu_exams.add_command(label='Химия', command=chem)
        menu_exams.add_command(label='Обществознание', command=obsh)
        menu_exams.add_command(label='Творческий конкурс Дизайн', command=des)
        menu_exams.add_command(label='Физика', command=phys)
        menu_exams.add_command(label='География', command=geo)
        menu_exams.add_command(label='Информатика', command=info)
        menu_exams.add_command(label='Творческий конкурс Медиа', command=Media)
        menu_exams.add_command(label='Творческий конкурс Мода', command=Moda)
        menu_exams.add_command(label='Творческий конкурс I этап', command=I_etap)
        mainmenu.add_cascade(label="тема", menu=menu1)
        mainmenu.add_command(label="Exit", command=window.destroy)
        mainmenu.add_cascade(label="список экзаменов", menu=menu_exams)
        window.config(menu=mainmenu)

        exam_var = tk.StringVar()
        exam_var.set("Введите название экзамена")
        name = tk.Entry(left, width=35, font=("Times", 20), textvariable=exam_var)
        name.pack(side="top")

        points_var = tk.StringVar()
        points_var.set("Введите количество баллов")
        points_entry = tk.Entry(left, width=25, font=("Times", 20), textvariable=points_var)
        points_entry.pack(side="top")

        big_var = tk.BooleanVar()
        big_var.set(False)
        big = tk.Checkbutton(left, text='>',
                             font=("Times", 20),
                             variable=big_var,
                             onvalue=True,
                             offvalue=False)
        big.pack(side="top")

        little_var = tk.BooleanVar()
        little_var.set(False)
        little = tk.Checkbutton(left,
                                text='<',
                                font=("Times", 20),
                                variable=little_var,
                                onvalue=True,
                                offvalue=False)
        little.pack(side="top")

        equally_var = tk.BooleanVar()
        equally_var.set(False)
        equally = tk.Checkbutton(left,
                                 text='=',
                                 font=("Times", 20),
                                 variable=equally_var,
                                 onvalue=True,
                                 offvalue=False)
        equally.pack(side="top")

        def clear_input():
            big_var.set(False)
            little_var.set(False)
            equally_var.set(False)
            points_var.set("Введите количество баллов")
            exam_var.set("Введите название экзамена")

        clear = tk.Button(left, text="Очистить выбор", font=("Times", 10), background="white", command=clear_input)
        clear.pack(side="top")

        start = tk.Button(left, text="запустить", font=("Times", 10), background="white",
                          command=get_snils_create_table)
        start.pack(side="top")

        path_xlsx_var = tk.StringVar()
        path_xlsx_var.set("Введите путь для сохранения xlsx файла")
        path_xlsx = tk.Entry(left, width=35, font=("Times", 20), textvariable=path_xlsx_var)
        path_xlsx.pack(side="top")

        name_xlsx_var = tk.StringVar()
        name_xlsx_var.set("Введите название xlsx файла")
        name_xlsx = tk.Entry(left, width=35, font=("Times", 20), textvariable=name_xlsx_var)
        name_xlsx.pack(side="top")

        create_graph_var = tk.BooleanVar()
        create_graph_var.set(False)
        create_graph = tk.Checkbutton(left, text='Создать и сохранить график',
                                      font=("Times", 20),
                                      variable=create_graph_var,
                                      onvalue=True,
                                      offvalue=False)
        create_graph.pack(side="top")

        path_graph_var = tk.StringVar()
        path_graph_var.set("Введите путь для сохранения png графика")
        path_graph = tk.Entry(left, width=35, font=("Times", 20), textvariable=path_graph_var)
        path_graph.pack(side="top")

        name_graph_var = tk.StringVar()
        name_graph_var.set("Введите название png графика")
        name_graph = tk.Entry(left, width=35, font=("Times", 20), textvariable=name_graph_var)
        name_graph.pack(side="top")

        save_button = tk.Button(left, text="сохранить", font=("Times", 10), background="white", command=save_get_snils)
        save_button.pack(side="top")

        message = """
        Данная функция показывает людей согласно их баллам.
        Таким образом можно проанализировать людей
        с необходимым количеством баллов.
        """
        # " "
        subscribe = tk.Label(left, text=message, font=("Times", 15))
        subscribe.pack(side="top")


    def places():
        window = tk.Toplevel()
        window.geometry("1000x900")
        style = ttk.Style(window)
        style.theme_use("clam")

        def fixed_map(option):
            return [elm for elm in
                    style.map('Treeview', background="white", fieldbackground="white", foreground="black") if
                    elm[:2] != ('!disabled', '!selected')]

        table = ttk.Treeview(window, columns=("Образовательная программа", "Бюджетные места", "Платные места"))
        table.column('#0', width=0, stretch="no")
        table.column('Образовательная программа', anchor="center", width=120)
        table.column('Бюджетные места', anchor="center", width=120)
        table.column('Платные места', anchor="center", width=120)
        table.heading('#0', text='', anchor="center")
        table.heading('Образовательная программа', text='Образовательная программа', anchor="center")
        table.heading('Бюджетные места', text='Бюджетные места', anchor="center")
        table.heading('Платные места', text='Платные места', anchor="center")
        table.pack(side="right", fill="both", expand=True)

        def night_theme():
            window.config(bg="#3E3D45")
            left.config(bg="#3E3D45")
            name.config(bg="#3E3D45", fg="#E1DFEE")
            paid.config(bg="#3E3D45", fg="#E1DFEE", selectcolor="#3E3D45")
            budget.config(bg="#3E3D45", fg="#E1DFEE", selectcolor="#3E3D45")
            clear.config(bg="#3E3D45", fg="#E1DFEE")
            start.config(bg="#3E3D45", fg="#E1DFEE")
            path_xlsx.config(bg="#3E3D45", fg="#E1DFEE")
            name_xlsx.config(bg="#3E3D45", fg="#E1DFEE")
            create_graph.config(bg="#3E3D45", fg="#E1DFEE", selectcolor="#3E3D45")
            path_graph.config(bg="#3E3D45", fg="#E1DFEE")
            name_graph.config(bg="#3E3D45", fg="#E1DFEE")
            save_button.config(bg="#3E3D45", fg="#E1DFEE")
            subscribe.config(bg="#3E3D45", fg="#E1DFEE")
            style.map('Treeview', foreground=fixed_map('foreground'),
                      background=fixed_map('background'))
            style.configure("Treeview", background="#3E3D45",
                            fieldbackground="#3E3D45",
                            foreground="#E1DFEE")

        def day_theme():
            window.config(bg="#f0f0f0")
            left.config(bg="#f0f0f0")
            name.config(bg="white", fg="#000000")
            paid.config(bg="#f0f0f0", fg="#000000")
            budget.config(bg="#f0f0f0", fg="#000000")
            clear.config(bg="white", fg="#000000")
            start.config(bg="white", fg="#000000")
            path_xlsx.config(bg="white", fg="#000000")
            name_xlsx.config(bg="white", fg="#000000")
            create_graph.config(bg="#f0f0f0", fg="#000000")
            path_graph.config(bg="white", fg="#000000")
            name_graph.config(bg="white", fg="#000000")
            save_button.config(bg="white", fg="#000000")
            subscribe.config(bg="#f0f0f0", fg="#000000")
            style.map('Treeview', foreground=fixed_map('foreground'),
                      background=fixed_map('background'))
            style.configure("Treeview", background="white",
                            fieldbackground="white",
                            foreground="black")

        def places_create_table():
            table.delete(*table.get_children())
            m = Places_for_education(ed_progaram_var.get(), budget_var.get(), paid_var.get())
            x = 0
            for i in m[0].iterrows():
                rowLabels = m[0].index.tolist()
                table.insert('', x, text=rowLabels[x], values=m[0].iloc[x, :].tolist())
                x += 1

        def save_places():
            n = Places_for_education(ed_progaram_var.get(), budget_var.get(), paid_var.get())
            save_file(n[0], name_xlsx_var.get(), path_xlsx_var.get())
            if create_graph_var.get() == True:
                save_file(n[1], name_graph_var.get(), path_graph_var.get())
                graph_window(name_graph_var.get(), path_graph_var.get())

        ed_progaram_var = tk.StringVar()
        ed_progaram_var.set("Введите название образовательной программы")

        def ep0():
            ed_progaram_var.set('Античность')

        def ep1():
            ed_progaram_var.set('Арабистика: язык, словесность, культура')

        def ep2():
            ed_progaram_var.set('Бизнес-информатика')

        def ep3():
            ed_progaram_var.set('Клеточная и молекулярная биотехнология')

        def ep4():
            ed_progaram_var.set('Юриспруденция: частное право')

        def ep5():
            ed_progaram_var.set('Дизайн')

        def ep6():
            ed_progaram_var.set('Программа двух дипломов НИУ ВШЭ и Университета Кёнхи Экономика ')

        def ep7():
            ed_progaram_var.set('Филология')

        def ep8():
            ed_progaram_var.set('Философия')

        def ep9():
            ed_progaram_var.set('Физика')

        def ep10():
            ed_progaram_var.set('Фундаментальная и компьютерная лингвистика')

        def ep11():
            ed_progaram_var.set('География глобальных изменений и геоинформационные технологии')

        def ep12():
            ed_progaram_var.set('Государственное и муниципальное управление')

        def ep13():
            ed_progaram_var.set('Городское планирование')

        def ep14():
            ed_progaram_var.set('Информационная безопасность')

        def ep15():
            ed_progaram_var.set('Иностранные языки и межкультурная коммуникация')

        def ep16():
            ed_progaram_var.set('История искусств')

        def ep17():
            ed_progaram_var.set('История')

        def ep18():
            ed_progaram_var.set('Инфокоммуникационные технологии и системы связи')

        def ep19():
            ed_progaram_var.set('Юриспруденция')

        def ep20():
            ed_progaram_var.set('Информатика и вычислительная техника')

        def ep21():
            ed_progaram_var.set('Компьютерная безопасность')

        def ep22():
            ed_progaram_var.set('Химия')

        def ep23():
            ed_progaram_var.set('Христианский Восток')

        def ep24():
            ed_progaram_var.set('Язык, словесность и культура Китая')

        def ep25():
            ed_progaram_var.set('Компьютерные науки и анализ данных')

        def ep26():
            ed_progaram_var.set('Культурология')

        def ep27():
            ed_progaram_var.set('Логистика и управление цепями поставок')

        def ep28():
            ed_progaram_var.set('Маркетинг и рыночная аналитика')

        def ep29():
            ed_progaram_var.set('Математика')

        def ep30():
            ed_progaram_var.set('Медиакоммуникации')

        def ep31():
            ed_progaram_var.set('Мировая экономика')

        def ep32():
            ed_progaram_var.set('Международные отношения')

        def ep33():
            ed_progaram_var.set('Мода')

        def ep34():
            ed_progaram_var.set('Программа двух дипломов НИУ ВШЭ и Лондонского университета по ме')

        def ep35():
            ed_progaram_var.set('Программная инженерия')

        def ep36():
            ed_progaram_var.set('Прикладная математика')

        def ep37():
            ed_progaram_var.set('Прикладная математика и информатика')

        def ep38():
            ed_progaram_var.set('Политология')

        def ep39():
            ed_progaram_var.set('Программа двух дипломов НИУ ВШЭ и Лондонского университета Прик')

        def ep40():
            ed_progaram_var.set('Психология')

        def ep41():
            ed_progaram_var.set('Реклама и связи с общественностью')

        def ep42():
            ed_progaram_var.set('Социология')

        def ep43():
            ed_progaram_var.set('Современное искусство')

        def ep44():
            ed_progaram_var.set('Экономика и статистика')

        def ep45():
            ed_progaram_var.set('Цифровые инновации в управлении предприятием (программа двух дип')

        def ep46():
            ed_progaram_var.set('Совместный бакалавриат НИУ ВШЭ и ЦПМ')

        def ep47():
            ed_progaram_var.set('Управление бизнесом')

        def ep48():
            ed_progaram_var.set('Востоковедение')

        def ep49():
            ed_progaram_var.set('Журналистика')

        mainmenu = tk.Menu(window, tearoff=0)
        menu1 = tk.Menu(mainmenu, tearoff=0)
        menu1.add_command(label='Тёмная тема', command=night_theme)
        menu1.add_command(label='Светлая тема', command=day_theme)
        menu_ed_program = tk.Menu(mainmenu, tearoff=0)
        menu_ed_program.add_command(label='Античность', command=ep0)
        menu_ed_program.add_command(label='Арабистика: язык, словесность, культура', command=ep1)
        menu_ed_program.add_command(label='Бизнес-информатика', command=ep2)
        menu_ed_program.add_command(label='Клеточная и молекулярная биотехнология', command=ep3)
        menu_ed_program.add_command(label='Юриспруденция: частное право', command=ep4)
        menu_ed_program.add_command(label='Дизайн', command=ep5)
        menu_ed_program.add_command(label='Программа двух дипломов НИУ ВШЭ и Университета Кёнхи Экономика ',
                                    command=ep6)
        menu_ed_program.add_command(label='Филология', command=ep7)
        menu_ed_program.add_command(label='Философия', command=ep8)
        menu_ed_program.add_command(label='Физика', command=ep9)
        menu_ed_program.add_command(label='Фундаментальная и компьютерная лингвистика', command=ep10)
        menu_ed_program.add_command(label='География глобальных изменений и геоинформационные технологии', command=ep11)
        menu_ed_program.add_command(label='Государственное и муниципальное управление', command=ep12)
        menu_ed_program.add_command(label='Городское планирование', command=ep13)
        menu_ed_program.add_command(label='Информационная безопасность', command=ep14)
        menu_ed_program.add_command(label='Иностранные языки и межкультурная коммуникация', command=ep15)
        menu_ed_program.add_command(label='История искусств', command=ep16)
        menu_ed_program.add_command(label='История', command=ep17)
        menu_ed_program.add_command(label='Инфокоммуникационные технологии и системы связи', command=ep18)
        menu_ed_program.add_command(label='Юриспруденция', command=ep19)
        menu_ed_program.add_command(label='Информатика и вычислительная техника', command=ep20)
        menu_ed_program.add_command(label='Компьютерная безопасность', command=ep21)
        menu_ed_program.add_command(label='Химия', command=ep22)
        menu_ed_program.add_command(label='Христианский Восток', command=ep23)
        menu_ed_program.add_command(label='Язык, словесность и культура Китая', command=ep24)
        menu_ed_program.add_command(label='Компьютерные науки и анализ данных', command=ep25)
        menu_ed_program.add_command(label='Культурология', command=ep26)
        menu_ed_program.add_command(label='Логистика и управление цепями поставок', command=ep27)
        menu_ed_program.add_command(label='Маркетинг и рыночная аналитика', command=ep28)
        menu_ed_program.add_command(label='Математика', command=ep29)
        menu_ed_program.add_command(label='Медиакоммуникации', command=ep30)
        menu_ed_program.add_command(label='Мировая экономика', command=ep31)
        menu_ed_program.add_command(label='Международные отношения', command=ep32)
        menu_ed_program.add_command(label='Мода', command=ep33)
        menu_ed_program.add_command(label='Программа двух дипломов НИУ ВШЭ и Лондонского университета по ме',
                                    command=ep34)
        menu_ed_program.add_command(label='Программная инженерия', command=ep35)
        menu_ed_program.add_command(label='Прикладная математика', command=ep36)
        menu_ed_program.add_command(label='Прикладная математика и информатика', command=ep37)
        menu_ed_program.add_command(label='Политология', command=ep38)
        menu_ed_program.add_command(label='Программа двух дипломов НИУ ВШЭ и Лондонского университета Прик',
                                    command=ep39)
        menu_ed_program.add_command(label='Психология', command=ep40)
        menu_ed_program.add_command(label='Реклама и связи с общественностью', command=ep41)
        menu_ed_program.add_command(label='Социология', command=ep42)
        menu_ed_program.add_command(label='Современное искусство', command=ep43)
        menu_ed_program.add_command(label='Экономика и статистика', command=ep44)
        menu_ed_program.add_command(label='Цифровые инновации в управлении предприятием (программа двух дип',
                                    command=ep45)
        menu_ed_program.add_command(label='Совместный бакалавриат НИУ ВШЭ и ЦПМ', command=ep46)
        menu_ed_program.add_command(label='Управление бизнесом', command=ep47)
        menu_ed_program.add_command(label='Востоковедение', command=ep48)
        menu_ed_program.add_command(label='Журналистика', command=ep49)
        mainmenu.add_cascade(label="тема", menu=menu1)
        mainmenu.add_command(label="Exit", command=window.destroy)
        mainmenu.add_cascade(label="Образовательная программа", menu=menu_ed_program)
        window.config(menu=mainmenu)

        left = tk.Frame(window)
        left.pack(side="left")

        name = tk.Entry(left, width=35, font=("Times", 20), textvariable=ed_progaram_var)
        name.pack(side="top")

        budget_var = tk.BooleanVar()
        budget_var.set(False)
        budget = tk.Checkbutton(left,
                                text="Убрать обр.программы с бюджетными местами",
                                font=("Times", 20),
                                variable=budget_var,
                                onvalue=True,
                                offvalue=False)
        budget.pack(side="top")

        paid_var = tk.BooleanVar()
        paid_var.set(False)
        paid = tk.Checkbutton(left,
                              text="Убрать обр.программы с платными местами",
                              font=("Times", 20),
                              variable=paid_var,
                              onvalue=True,
                              offvalue=False)
        paid.pack(side="top")

        def clear_input():
            budget_var.set(False)
            paid_var.set(False)
            ed_progaram_var.set("Введите название образовательной программы")

        clear = tk.Button(left, text="Очистить выбор", font=("Times", 10), background="white", command=clear_input)
        clear.pack(side="top")

        start = tk.Button(left, text="запустить", font=("Times", 10), background="white", command=places_create_table)
        start.pack(side="top")

        path_xlsx_var = tk.StringVar()
        path_xlsx_var.set("Введите путь для сохранения xlsx файла")
        path_xlsx = tk.Entry(left, width=35, font=("Times", 20), textvariable=path_xlsx_var)
        path_xlsx.pack(side="top")

        name_xlsx_var = tk.StringVar()
        name_xlsx_var.set("Введите название xlsx файла")
        name_xlsx = tk.Entry(left, width=35, font=("Times", 20), textvariable=name_xlsx_var)
        name_xlsx.pack(side="top")

        create_graph_var = tk.BooleanVar()
        create_graph_var.set(False)
        create_graph = tk.Checkbutton(left, text='Создать и сохранить график',
                                      font=("Times", 20),
                                      variable=create_graph_var,
                                      onvalue=True,
                                      offvalue=False)
        create_graph.pack(side="top")

        path_graph_var = tk.StringVar()
        path_graph_var.set("Введите путь для сохранения png графика")
        path_graph = tk.Entry(left, width=35, font=("Times", 20), textvariable=path_graph_var)
        path_graph.pack(side="top")

        name_graph_var = tk.StringVar()
        name_graph_var.set("Введите название png графика")
        name_graph = tk.Entry(left, width=35, font=("Times", 20), textvariable=name_graph_var)
        name_graph.pack(side="top")

        save_button = tk.Button(left, text="сохранить", font=("Times", 10), background="white", command=save_places)
        save_button.pack(side="top")

        message = """
        Эта функция позволяет увидеть таблицу 
        доступных образовательных программ 
        и доступных мест для поступления.
        """
        # " "
        subscribe = tk.Label(left, text=message, font=("Times", 15))
        subscribe.pack(side="top")


    def Entrant_data():
        window = tk.Toplevel()
        window.geometry("1700x900")
        style = ttk.Style(window)
        style.theme_use("clam")

        def fixed_map(option):
            return [elm for elm in
                    style.map('Treeview', background="white", fieldbackground="white", foreground="black") if
                    elm[:2] != ('!disabled', '!selected')]

        table = ttk.Treeview(window,
                             columns=("N",
                                      "СНИЛС",
                                      "Без испытаний",
                                      "Особое право",
                                      "Целевая квота",
                                      "Программа",
                                      "Сумма баллов"))
        table.column('#0', width=0, stretch="no")
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
        table.pack(side="right", fill="both", expand=True)

        def night_theme():
            window.config(bg="#3E3D45")
            left.config(bg="#3E3D45")
            right.config(bg="#3E3D45", fg="#E1DFEE", selectcolor="#3E3D45")
            no_right.config(bg="#3E3D45", fg="#E1DFEE", selectcolor="#3E3D45")
            special.config(bg="#3E3D45", fg="#E1DFEE", selectcolor="#3E3D45")
            no_special.config(bg="#3E3D45", fg="#E1DFEE", selectcolor="#3E3D45")
            target.config(bg="#3E3D45", fg="#E1DFEE", selectcolor="#3E3D45")
            no_target.config(bg="#3E3D45", fg="#E1DFEE", selectcolor="#3E3D45")
            name.config(bg="#3E3D45", fg="#E1DFEE")
            points_entry.config(bg="#3E3D45", fg="#E1DFEE")
            big.config(bg="#3E3D45", fg="#E1DFEE", selectcolor="#3E3D45")
            little.config(bg="#3E3D45", fg="#E1DFEE", selectcolor="#3E3D45")
            equally.config(bg="#3E3D45", fg="#E1DFEE", selectcolor="#3E3D45")
            clear.config(bg="#3E3D45", fg="#E1DFEE")
            start.config(bg="#3E3D45", fg="#E1DFEE")
            path_xlsx.config(bg="#3E3D45", fg="#E1DFEE")
            name_xlsx.config(bg="#3E3D45", fg="#E1DFEE")
            save_button.config(bg="#3E3D45", fg="#E1DFEE")
            subscribe.config(bg="#3E3D45", fg="#E1DFEE")
            style.map('Treeview', foreground=fixed_map('foreground'),
                      background=fixed_map('background'))
            style.configure("Treeview", background="#3E3D45",
                            fieldbackground="#3E3D45",
                            foreground="#E1DFEE")

        def day_theme():
            window.config(bg="#f0f0f0")
            left.config(bg="#f0f0f0")
            right.config(bg="#f0f0f0", fg="#000000")
            no_right.config(bg="#f0f0f0", fg="#000000")
            special.config(bg="#f0f0f0", fg="#000000")
            no_special.config(bg="#f0f0f0", fg="#000000")
            target.config(bg="#f0f0f0", fg="#000000")
            no_target.config(bg="#f0f0f0", fg="#000000")
            name.config(bg="white", fg="#000000")
            points_entry.config(bg="white", fg="#000000")
            big.config(bg="#f0f0f0", fg="#000000")
            little.config(bg="#f0f0f0", fg="#000000")
            equally.config(bg="#f0f0f0", fg="#000000")
            clear.config(bg="white", fg="#000000")
            start.config(bg="white", fg="#000000")
            path_xlsx.config(bg="white", fg="#000000")
            name_xlsx.config(bg="white", fg="#000000")
            save_button.config(bg="white", fg="#000000")
            subscribe.config(bg="#f0f0f0", fg="#000000")
            style.map('Treeview', foreground=fixed_map('foreground'),
                      background=fixed_map('background'))
            style.configure("Treeview", background="white",
                            fieldbackground="white",
                            foreground="black")

        def entrant_data_create_table():
            table.delete(*table.get_children())
            operator = ''
            if little_var.get() == True:
                operator = operator + '<'
            if big_var.get() == True:
                operator = operator + '>'
            if equally_var.get() == True:
                operator = operator + '='
            m = entrant_data(without_exam_var.get(),
                             special_q_var.get(),
                             target_q_var.get(),
                             ed_progaram_var.get(),
                             points_var.get(),
                             operator)
            x = 0
            for i in m.iterrows():
                rowLabels = m.index.tolist()
                table.insert('', x, text=rowLabels[x], values=m.iloc[x, :].tolist())
                x += 1

        def save_Entrant_data():
            operator = ''
            if little_var.get() == True:
                operator = operator + '<'
            if big_var.get() == True:
                operator = operator + '>'
            if equally_var.get() == True:
                operator = operator + '='
            m = entrant_data(without_exam_var.get(),
                             special_q_var.get(),
                             target_q_var.get(),
                             ed_progaram_var.get(),
                             points_var.get(),
                             operator)
            save_file(m, name_xlsx_var.get(), path_xlsx_var.get())

        ed_progaram_var = tk.StringVar()
        ed_progaram_var.set("Введите название образовательной программы")

        def ep0():
            ed_progaram_var.set('Античность')

        def ep1():
            ed_progaram_var.set('Арабистика: язык, словесность, культура')

        def ep2():
            ed_progaram_var.set('Бизнес-информатика')

        def ep3():
            ed_progaram_var.set('Клеточная и молекулярная биотехнология')

        def ep4():
            ed_progaram_var.set('Юриспруденция: частное право')

        def ep5():
            ed_progaram_var.set('Дизайн')

        def ep6():
            ed_progaram_var.set('Программа двух дипломов НИУ ВШЭ и Университета Кёнхи Экономика ')

        def ep7():
            ed_progaram_var.set('Филология')

        def ep8():
            ed_progaram_var.set('Философия')

        def ep9():
            ed_progaram_var.set('Физика')

        def ep10():
            ed_progaram_var.set('Фундаментальная и компьютерная лингвистика')

        def ep11():
            ed_progaram_var.set('География глобальных изменений и геоинформационные технологии')

        def ep12():
            ed_progaram_var.set('Государственное и муниципальное управление')

        def ep13():
            ed_progaram_var.set('Городское планирование')

        def ep14():
            ed_progaram_var.set('Информационная безопасность')

        def ep15():
            ed_progaram_var.set('Иностранные языки и межкультурная коммуникация')

        def ep16():
            ed_progaram_var.set('История искусств')

        def ep17():
            ed_progaram_var.set('История')

        def ep18():
            ed_progaram_var.set('Инфокоммуникационные технологии и системы связи')

        def ep19():
            ed_progaram_var.set('Юриспруденция')

        def ep20():
            ed_progaram_var.set('Информатика и вычислительная техника')

        def ep21():
            ed_progaram_var.set('Компьютерная безопасность')

        def ep22():
            ed_progaram_var.set('Химия')

        def ep23():
            ed_progaram_var.set('Христианский Восток')

        def ep24():
            ed_progaram_var.set('Язык, словесность и культура Китая')

        def ep25():
            ed_progaram_var.set('Компьютерные науки и анализ данных')

        def ep26():
            ed_progaram_var.set('Культурология')

        def ep27():
            ed_progaram_var.set('Логистика и управление цепями поставок')

        def ep28():
            ed_progaram_var.set('Маркетинг и рыночная аналитика')

        def ep29():
            ed_progaram_var.set('Математика')

        def ep30():
            ed_progaram_var.set('Медиакоммуникации')

        def ep31():
            ed_progaram_var.set('Мировая экономика')

        def ep32():
            ed_progaram_var.set('Международные отношения')

        def ep33():
            ed_progaram_var.set('Мода')

        def ep34():
            ed_progaram_var.set('Программа двух дипломов НИУ ВШЭ и Лондонского университета по ме')

        def ep35():
            ed_progaram_var.set('Программная инженерия')

        def ep36():
            ed_progaram_var.set('Прикладная математика')

        def ep37():
            ed_progaram_var.set('Прикладная математика и информатика')

        def ep38():
            ed_progaram_var.set('Политология')

        def ep39():
            ed_progaram_var.set('Программа двух дипломов НИУ ВШЭ и Лондонского университета Прик')

        def ep40():
            ed_progaram_var.set('Психология')

        def ep41():
            ed_progaram_var.set('Реклама и связи с общественностью')

        def ep42():
            ed_progaram_var.set('Социология')

        def ep43():
            ed_progaram_var.set('Современное искусство')

        def ep44():
            ed_progaram_var.set('Экономика и статистика')

        def ep45():
            ed_progaram_var.set('Цифровые инновации в управлении предприятием (программа двух дип')

        def ep46():
            ed_progaram_var.set('Совместный бакалавриат НИУ ВШЭ и ЦПМ')

        def ep47():
            ed_progaram_var.set('Управление бизнесом')

        def ep48():
            ed_progaram_var.set('Востоковедение')

        def ep49():
            ed_progaram_var.set('Журналистика')

        mainmenu = tk.Menu(window, tearoff=0)
        menu1 = tk.Menu(mainmenu, tearoff=0)
        menu1.add_command(label='Тёмная тема', command=night_theme)
        menu1.add_command(label='Светлая тема', command=day_theme)
        menu_ed_program = tk.Menu(mainmenu, tearoff=0)
        menu_ed_program.add_command(label='Античность', command=ep0)
        menu_ed_program.add_command(label='Арабистика: язык, словесность, культура', command=ep1)
        menu_ed_program.add_command(label='Бизнес-информатика', command=ep2)
        menu_ed_program.add_command(label='Клеточная и молекулярная биотехнология', command=ep3)
        menu_ed_program.add_command(label='Юриспруденция: частное право', command=ep4)
        menu_ed_program.add_command(label='Дизайн', command=ep5)
        menu_ed_program.add_command(label='Программа двух дипломов НИУ ВШЭ и Университета Кёнхи Экономика ',
                                    command=ep6)
        menu_ed_program.add_command(label='Филология', command=ep7)
        menu_ed_program.add_command(label='Философия', command=ep8)
        menu_ed_program.add_command(label='Физика', command=ep9)
        menu_ed_program.add_command(label='Фундаментальная и компьютерная лингвистика', command=ep10)
        menu_ed_program.add_command(label='География глобальных изменений и геоинформационные технологии', command=ep11)
        menu_ed_program.add_command(label='Государственное и муниципальное управление', command=ep12)
        menu_ed_program.add_command(label='Городское планирование', command=ep13)
        menu_ed_program.add_command(label='Информационная безопасность', command=ep14)
        menu_ed_program.add_command(label='Иностранные языки и межкультурная коммуникация', command=ep15)
        menu_ed_program.add_command(label='История искусств', command=ep16)
        menu_ed_program.add_command(label='История', command=ep17)
        menu_ed_program.add_command(label='Инфокоммуникационные технологии и системы связи', command=ep18)
        menu_ed_program.add_command(label='Юриспруденция', command=ep19)
        menu_ed_program.add_command(label='Информатика и вычислительная техника', command=ep20)
        menu_ed_program.add_command(label='Компьютерная безопасность', command=ep21)
        menu_ed_program.add_command(label='Химия', command=ep22)
        menu_ed_program.add_command(label='Христианский Восток', command=ep23)
        menu_ed_program.add_command(label='Язык, словесность и культура Китая', command=ep24)
        menu_ed_program.add_command(label='Компьютерные науки и анализ данных', command=ep25)
        menu_ed_program.add_command(label='Культурология', command=ep26)
        menu_ed_program.add_command(label='Логистика и управление цепями поставок', command=ep27)
        menu_ed_program.add_command(label='Маркетинг и рыночная аналитика', command=ep28)
        menu_ed_program.add_command(label='Математика', command=ep29)
        menu_ed_program.add_command(label='Медиакоммуникации', command=ep30)
        menu_ed_program.add_command(label='Мировая экономика', command=ep31)
        menu_ed_program.add_command(label='Международные отношения', command=ep32)
        menu_ed_program.add_command(label='Мода', command=ep33)
        menu_ed_program.add_command(label='Программа двух дипломов НИУ ВШЭ и Лондонского университета по ме',
                                    command=ep34)
        menu_ed_program.add_command(label='Программная инженерия', command=ep35)
        menu_ed_program.add_command(label='Прикладная математика', command=ep36)
        menu_ed_program.add_command(label='Прикладная математика и информатика', command=ep37)
        menu_ed_program.add_command(label='Политология', command=ep38)
        menu_ed_program.add_command(label='Программа двух дипломов НИУ ВШЭ и Лондонского университета Прик',
                                    command=ep39)
        menu_ed_program.add_command(label='Психология', command=ep40)
        menu_ed_program.add_command(label='Реклама и связи с общественностью', command=ep41)
        menu_ed_program.add_command(label='Социология', command=ep42)
        menu_ed_program.add_command(label='Современное искусство', command=ep43)
        menu_ed_program.add_command(label='Экономика и статистика', command=ep44)
        menu_ed_program.add_command(label='Цифровые инновации в управлении предприятием (программа двух дип',
                                    command=ep45)
        menu_ed_program.add_command(label='Совместный бакалавриат НИУ ВШЭ и ЦПМ', command=ep46)
        menu_ed_program.add_command(label='Управление бизнесом', command=ep47)
        menu_ed_program.add_command(label='Востоковедение', command=ep48)
        menu_ed_program.add_command(label='Журналистика', command=ep49)
        mainmenu.add_cascade(label="тема", menu=menu1)
        mainmenu.add_command(label="Exit", command=window.destroy)
        mainmenu.add_cascade(label="Образовательная программа", menu=menu_ed_program)
        window.config(menu=mainmenu)

        left = tk.Frame(window)
        left.pack(side="left")

        without_exam_var = tk.StringVar()
        without_exam_var.set('')
        right = tk.Radiobutton(left,
                               text="Убрать абитуриентов с правом без экзаменов",
                               font=("Times", 20), variable=without_exam_var,
                               value='0')
        right.pack(side="top")
        no_right = tk.Radiobutton(left,
                                  text="Убрать абитуриентов без права без экзаменов",
                                  font=("Times", 20),
                                  variable=without_exam_var,
                                  value='1')
        no_right.pack(side="top")

        special_q_var = tk.StringVar()
        special_q_var.set('')
        special = tk.Radiobutton(left,
                                 text="Убрать абитуриентов с особой квотой",
                                 font=("Times", 20),
                                 variable=special_q_var,
                                 value='0')
        special.pack(side="top")
        no_special = tk.Radiobutton(left,
                                    text="Убрать абитуриентов без особой квоты",
                                    font=("Times", 20),
                                    variable=special_q_var,
                                    value='1')
        no_special.pack(side="top")

        target_q_var = tk.StringVar()
        target_q_var.set('')
        target = tk.Radiobutton(left,
                                text="Убрать абитуриентов с целевой квотой",
                                font=("Times", 20),
                                variable=target_q_var,
                                value='0')
        target.pack(side="top")

        no_target = tk.Radiobutton(left,
                                   text="Убрать абитуриентов без целевой квоты",
                                   font=("Times", 20),
                                   variable=target_q_var,
                                   value='1')
        no_target.pack(side="top")

        name = tk.Entry(left, width=35, font=("Times", 20), textvariable=ed_progaram_var)
        name.pack(side="top")

        points_var = tk.StringVar()
        points_var.set("Введите количество баллов")
        points_entry = tk.Entry(left, width=25, font=("Times", 20), textvariable=points_var)
        points_entry.pack(side="top")

        big_var = tk.BooleanVar()
        big_var.set(False)
        big = tk.Checkbutton(left, text='>',
                             font=("Times", 20),
                             variable=big_var,
                             onvalue=True,
                             offvalue=False)
        big.pack(side="top")

        little_var = tk.BooleanVar()
        little_var.set(False)
        little = tk.Checkbutton(left,
                                text='<',
                                font=("Times", 20),
                                variable=little_var,
                                onvalue=True,
                                offvalue=False)
        little.pack(side="top")

        equally_var = tk.BooleanVar()
        equally_var.set(False)
        equally = tk.Checkbutton(left,
                                 text='=',
                                 font=("Times", 20),
                                 variable=equally_var,
                                 onvalue=True,
                                 offvalue=False)
        equally.pack(side="top")

        def clear_input():
            without_exam_var.set('')
            special_q_var.set('')
            target_q_var.set('')
            big_var.set(False)
            little_var.set(False)
            equally_var.set(False)
            points_var.set("Введите количество баллов")
            ed_progaram_var.set("Введите название образовательной программы")

        clear = tk.Button(left, text="Очистить выбор", font=("Times", 10), background="white", command=clear_input)
        clear.pack(side="top")

        start = tk.Button(left, text="запустить", font=("Times", 10), background="white",
                          command=entrant_data_create_table)
        start.pack(side="top")

        path_xlsx_var = tk.StringVar()
        path_xlsx_var.set("Введите путь для сохранения xlsx файла")
        path_xlsx = tk.Entry(left, width=35, font=("Times", 20), textvariable=path_xlsx_var)
        path_xlsx.pack(side="top")

        name_xlsx_var = tk.StringVar()
        name_xlsx_var.set("Введите название xlsx файла")
        name_xlsx = tk.Entry(left, width=35, font=("Times", 20), textvariable=name_xlsx_var)
        name_xlsx.pack(side="top")

        save_button = tk.Button(left, text="сохранить", font=("Times", 10), background="white",
                                command=save_Entrant_data)
        save_button.pack(side="top")

        message = """
        Функция позвляет
        получить данные об абитуриентах
        с определённой образовательной программы.
        """
        # " "
        subscribe = tk.Label(left, text=message, font=("Times", 15))
        subscribe.pack(side="top")


    def quota():
        window = tk.Toplevel()
        window.geometry("2000x900")

        style = ttk.Style(window)
        style.theme_use("clam")

        def fixed_map(option):
            return [elm for elm in
                    style.map('Treeview', background="white", fieldbackground="white", foreground="black") if
                    elm[:2] != ('!disabled', '!selected')]

        def night_theme():
            window.config(bg="#3E3D45")
            left.config(bg="#3E3D45")
            path_xlsx.config(bg="#3E3D45", fg="#E1DFEE")
            name_xlsx.config(bg="#3E3D45", fg="#E1DFEE")
            save_button.config(bg="#3E3D45", fg="#E1DFEE")
            subscribe.config(bg="#3E3D45", fg="#E1DFEE")
            style.map('Treeview', foreground=fixed_map('foreground'),
                      background=fixed_map('background'))
            style.configure("Treeview", background="#3E3D45",
                            fieldbackground="#3E3D45",
                            foreground="#E1DFEE")

        def day_theme():
            window.config(bg="#f0f0f0")
            left.config(bg="#f0f0f0")
            path_xlsx.config(bg="white", fg="#000000")
            name_xlsx.config(bg="white", fg="#000000")
            save_button.config(bg="white", fg="#000000")
            subscribe.config(bg="#f0f0f0", fg="#000000")
            style.map('Treeview', foreground=fixed_map('foreground'),
                      background=fixed_map('background'))
            style.configure("Treeview", background="white",
                            fieldbackground="white",
                            foreground="black")

        mainmenu = tk.Menu(window, tearoff=0)
        menu1 = tk.Menu(mainmenu, tearoff=0)
        menu1.add_command(label='Тёмная тема', command=night_theme)
        menu1.add_command(label='Светлая тема', command=day_theme)
        mainmenu.add_cascade(label="тема", menu=menu1)
        mainmenu.add_command(label="Exit", command=window.destroy)
        window.config(menu=mainmenu)

        table = ttk.Treeview(window, columns=("Программа",
                                              "Квота",
                                              'Литература',
                                              'Русский язык',
                                              'Иностранный язык',
                                              'История',
                                              'Математика',
                                              'Биология',
                                              'Химия',
                                              'Обществознание',
                                              'Творческий конкурс Дизайн',
                                              'Физика',
                                              'География',
                                              'Информатика',
                                              'Творческий конкурс Медиа',
                                              'Творческий конкурс Мода',
                                              'Творческий конкурс I этап'))
        table.column('#0', width=0, stretch="no")
        table.column('Программа', anchor="center", width=120)
        table.column('Квота', anchor="center", width=80)
        table.column('Литература', anchor="center", width=80)
        table.column('Русский язык', anchor="center", width=80)
        table.column('Иностранный язык', anchor="center", width=80)
        table.column('История', anchor="center", width=80)
        table.column('Математика', anchor="center", width=80)
        table.column('Биология', anchor="center", width=80)
        table.column('Химия', anchor="center", width=80)
        table.column('Обществознание', anchor="center", width=80)
        table.column('Творческий конкурс Дизайн', anchor="center", width=80)
        table.column('Физика', anchor="center", width=80)
        table.column('География', anchor="center", width=80)
        table.column('Информатика', anchor="center", width=80)
        table.column('Творческий конкурс Медиа', anchor="center", width=80)
        table.column('Творческий конкурс Мода', anchor="center", width=80)
        table.column('Творческий конкурс I этап', anchor="center", width=80)
        table.heading('#0', text='', anchor="center")
        table.heading('Программа', text='Программа', anchor="center")
        table.heading('Квота', text='Есть квота', anchor="center")
        table.heading('Литература', text='Литература', anchor="center")
        table.heading('Русский язык', text='Русский язык', anchor="center")
        table.heading('Иностранный язык', text='Иностранный язык', anchor="center")
        table.heading('История', text='История', anchor="center")
        table.heading('Математика', text='Математика', anchor="center")
        table.heading('Биология', text='Биология', anchor="center")
        table.heading('Химия', text='Химия', anchor="center")
        table.heading('Обществознание', text='Обществознание', anchor="center")
        table.heading('Творческий конкурс Дизайн', text='Творческий конкурс Дизайн', anchor="center")
        table.heading('Физика', text='Физика', anchor="center")
        table.heading('География', text='География', anchor="center")
        table.heading('Информатика', text='Информатика', anchor="center")
        table.heading('Творческий конкурс Медиа', text='Т.к. Медиа', anchor="center")
        table.heading('Творческий конкурс Мода', text='Т.к. Мода', anchor="center")
        table.heading('Творческий конкурс I этап', text='Т.к. I этап', anchor="center")
        table.pack(side="right", fill="both", expand=True)
        m = quota_program_breakdown_for_treeview()
        x = 0
        for i in m.iterrows():
            rowLabels = m.index.tolist()
            table.insert('', x, text=rowLabels[x], values=m.iloc[x, :].tolist())
            x += 1

        def save_quota():
            save_file(m, name_xlsx_var.get(), path_xlsx_var.get())

        left = tk.Frame(window)
        left.pack(side="left")

        path_xlsx_var = tk.StringVar()
        path_xlsx_var.set("Введите путь для сохранения xlsx файла")
        path_xlsx = tk.Entry(left, width=35, font=("Times", 20), textvariable=path_xlsx_var)
        path_xlsx.pack(side="top")

        name_xlsx_var = tk.StringVar()
        name_xlsx_var.set("Введите название xlsx файла")
        name_xlsx = tk.Entry(left, width=35, font=("Times", 20), textvariable=name_xlsx_var)
        name_xlsx.pack(side="top")

        save_button = tk.Button(left, text="сохранить", font=("Times", 10), background="white", command=save_quota)
        save_button.pack(side="top")

        message = """
        Данная функция позволяет пользователю 
        сравнить средний балл абитуриентов,
        проходящих по квоте, и абитуриентов без квоты.
        Причём рассматриваются только те абитуриенты, 
        которые подали согласие на зачисление 
        и не вернули документы.
        """
        # " "
        subscribe = tk.Label(left, text=message, font=("Times", 15))
        subscribe.pack(side="top")


    def without_exams():
        window = tk.Toplevel()
        window.geometry("2000x900")

        style = ttk.Style(window)
        style.theme_use("clam")

        def fixed_map(option):
            return [elm for elm in
                    style.map('Treeview', background="white", fieldbackground="white", foreground="black") if
                    elm[:2] != ('!disabled', '!selected')]

        def night_theme():
            window.config(bg="#3E3D45")
            left.config(bg="#3E3D45")
            path_xlsx.config(bg="#3E3D45", fg="#E1DFEE")
            name_xlsx.config(bg="#3E3D45", fg="#E1DFEE")
            save_button.config(bg="#3E3D45", fg="#E1DFEE")
            subscribe.config(bg="#3E3D45", fg="#E1DFEE")
            style.map('Treeview', foreground=fixed_map('foreground'),
                      background=fixed_map('background'))
            style.configure("Treeview", background="#3E3D45",
                            fieldbackground="#3E3D45",
                            foreground="#E1DFEE")

        def day_theme():
            window.config(bg="#f0f0f0")
            left.config(bg="#f0f0f0")
            path_xlsx.config(bg="white", fg="#000000")
            name_xlsx.config(bg="white", fg="#000000")
            save_button.config(bg="white", fg="#000000")
            subscribe.config(bg="#f0f0f0", fg="#000000")
            style.map('Treeview', foreground=fixed_map('foreground'),
                      background=fixed_map('background'))
            style.configure("Treeview", background="white",
                            fieldbackground="white",
                            foreground="black")

        mainmenu = tk.Menu(window, tearoff=0)
        menu1 = tk.Menu(mainmenu, tearoff=0)
        menu1.add_command(label='Тёмная тема', command=night_theme)
        menu1.add_command(label='Светлая тема', command=day_theme)
        mainmenu.add_cascade(label="тема", menu=menu1)
        mainmenu.add_command(label="Exit", command=window.destroy)
        window.config(menu=mainmenu)

        table = ttk.Treeview(window, columns=("Программа",
                                              "Квота",
                                              'Литература',
                                              'Русский язык',
                                              'Иностранный язык',
                                              'История',
                                              'Математика',
                                              'Биология',
                                              'Химия',
                                              'Обществознание',
                                              'Творческий конкурс Дизайн',
                                              'Физика',
                                              'География',
                                              'Информатика',
                                              'Творческий конкурс Медиа',
                                              'Творческий конкурс Мода',
                                              'Творческий конкурс I этап'))
        table.column('#0', width=0, stretch="no")
        table.column('Программа', anchor="center", width=120)
        table.column('Квота', anchor="center", width=80)
        table.column('Литература', anchor="center", width=80)
        table.column('Русский язык', anchor="center", width=80)
        table.column('Иностранный язык', anchor="center", width=80)
        table.column('История', anchor="center", width=80)
        table.column('Математика', anchor="center", width=80)
        table.column('Биология', anchor="center", width=80)
        table.column('Химия', anchor="center", width=80)
        table.column('Обществознание', anchor="center", width=80)
        table.column('Творческий конкурс Дизайн', anchor="center", width=80)
        table.column('Физика', anchor="center", width=80)
        table.column('География', anchor="center", width=80)
        table.column('Информатика', anchor="center", width=80)
        table.column('Творческий конкурс Медиа', anchor="center", width=80)
        table.column('Творческий конкурс Мода', anchor="center", width=80)
        table.column('Творческий конкурс I этап', anchor="center", width=80)
        table.heading('#0', text='', anchor="center")
        table.heading('Программа', text='Программа', anchor="center")
        table.heading('Квота', text='Есть квота', anchor="center")
        table.heading('Литература', text='Литература', anchor="center")
        table.heading('Русский язык', text='Русский язык', anchor="center")
        table.heading('Иностранный язык', text='Иностранный язык', anchor="center")
        table.heading('История', text='История', anchor="center")
        table.heading('Математика', text='Математика', anchor="center")
        table.heading('Биология', text='Биология', anchor="center")
        table.heading('Химия', text='Химия', anchor="center")
        table.heading('Обществознание', text='Обществознание', anchor="center")
        table.heading('Творческий конкурс Дизайн', text='Творческий конкурс Дизайн', anchor="center")
        table.heading('Физика', text='Физика', anchor="center")
        table.heading('География', text='География', anchor="center")
        table.heading('Информатика', text='Информатика', anchor="center")
        table.heading('Творческий конкурс Медиа', text='Т.к. Медиа', anchor="center")
        table.heading('Творческий конкурс Мода', text='Т.к. Мода', anchor="center")
        table.heading('Творческий конкурс I этап', text='Т.к. I этап', anchor="center")
        table.pack(side="right", fill="both", expand=True)
        m = right_program_breakdown_for_treeview()
        x = 0
        for i in m.iterrows():
            rowLabels = m.index.tolist()
            table.insert('', x, text=rowLabels[x], values=m.iloc[x, :].tolist())
            x += 1

        def save_without_exam():
            save_file(m, name_xlsx_var.get(), path_xlsx_var.get())

        left = tk.Frame(window)
        left.pack(side="left")

        path_xlsx_var = tk.StringVar()
        path_xlsx_var.set("Введите путь для сохранения xlsx файла")
        path_xlsx = tk.Entry(left, width=35, font=("Times", 20), textvariable=path_xlsx_var)
        path_xlsx.pack(side="top")

        name_xlsx_var = tk.StringVar()
        name_xlsx_var.set("Введите название xlsx файла")
        name_xlsx = tk.Entry(left, width=35, font=("Times", 20), textvariable=name_xlsx_var)
        name_xlsx.pack(side="top")

        save_button = tk.Button(left, text="сохранить", font=("Times", 10), background="white",
                                command=save_without_exam)
        save_button.pack(side="top")

        message = """
        Данная функция позволяет пользователю 
        сравнить средний балл абитуриентов,
        проходящих без вступительных испытаний, 
        и абитуриентов без такого права.
        Причём рассматриваются только те абитуриенты, 
        которые подали согласие на зачисление 
        и не вернули документы.
        """
        # " "
        subscribe = tk.Label(left, text=message, font=("Times", 15))
        subscribe.pack(side="top")


    root = tk.Tk()

    root.title("Welcome!")
    root.geometry("428x867+700+100")
    # root.wm_attributes('-transparentcolor', root['background'])

    path = "IMG_20220509_170259.jpg"
    img = Image.open(path)
    img = img.resize((428, 867), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)

    path2 = "IMG_20220509_170243.jpg"
    img2 = Image.open(path2)
    img2 = img2.resize((1300, 642), Image.ANTIALIAS)
    img2 = ImageTk.PhotoImage(img2)

    panel = tk.Label(root, image=img, cursor="star")
    panel.pack(side="bottom", fill="both", expand="yes")

    wel = tk.Label(panel, text="Welcome!", background="white", font=("Lucida Handwriting", 40), foreground="#5194ed")
    wel.pack()

    but = tk.Button(panel, text="start", font=("Lucida Handwriting", 40), background="white", foreground="#57612a",
                    command=new_window)
    but.pack(side="bottom")

    root.mainloop()
