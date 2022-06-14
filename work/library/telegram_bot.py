__all__ = ['get_telegram_graphs', 'create_telegram_bot']

import os
import time
import shutil

import pandas as pd

import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By

SNILS = None
autoupdate_interval = None
website_link = ''

flag_autoupdate = False
flag_update_interval = False
flag_SNILS = False


def get_telegram_graphs(final_scores, agreements, BVI_number, all_places):
    '''
    Выводит диаграмму с соотношением ЕГЭшников, олимпиадников, льготников.
    Также выводит график зависимости кол-ва поданных заявлений от кол-ва дней
    :param final_scores: список из суммы баллов по ЕГЭ для каждого абитуриента
    :param agreements: список, содержащий информацию о том, подал ли заявление каждый абитуриент
    :param BVI_number: кол-во олимпиадников
    :param all_places: общее кол-во конкурсных мест
    :return: Функция возвращает None
    '''
    pass


def create_telegram_bot():
    '''
    Создает телеграмм-бота
    :return: обьект, с помощью которого происходит управление ботом
    '''
    bot_token = '5484337995:AAESpTcLKz_vT4-1eHQWaBmlUeYskAr3vSY'
    bot = telebot.TeleBot(bot_token)

    @bot.message_handler(commands=['start'])
    def get_link(message):
        bot.send_message(message.from_user.id, 'Вставьте ссылку на гугл таблицу:')
        bot.register_next_step_handler(message, get_google_sheets)

    def get_google_sheets(message):
        global website_link
        flag_google_sheets = False
        while not os.path.exists('students.xlsx'):
            try:
                website_link = message.text
                parse_website_link(website_link)
            except:
                bot.reply_to(message, "Неправильная ссылка на гугл таблицу.")
                bot.send_message(message.from_user.id, 'Вставьте ссылку на гугл таблицу:')
                bot.register_next_step_handler(message, get_google_sheets)
                break
        if os.path.exists('students.xlsx') and not flag_google_sheets:
            flag_google_sheets = True
            bot.send_message(message.from_user.id, "Введите свой СНИЛС")
            bot.register_next_step_handler(message, get_SNILS)

    def get_SNILS(message):
        global SNILS, flag_SNILS
        SNILS = message.text
        while not is_SNILS_exist():
            bot.reply_to(message, "Ваш СНИЛС отсутствует в списке поступающих")
            get_google_sheets(message)
            break
        if is_SNILS_exist() and not flag_SNILS:
            flag_SNILS = True
            get_info(message)
            bot.send_message(message.from_user.id, "Чтобы вывести список всех команд, напишите /commands")

    @bot.message_handler(commands=['show'])
    def get_info(message):
        bot.send_message(message.from_user.id,
                         "Пожалуйста, подождите. Информация о месте в списке поступающих будет приведена ниже.")
        dicts_list_to_bot = To_Bot(SNILS)
        for element in dicts_list_to_bot:
            output_message = f'''
            ОП: {element['Образовательная программа']}
            Количество бюджетных мест: {element['Бюджетные места']}
            Проходите ли вы: {'Да' if element['get_budget_place'] == '+' else 'Нет'}
            '''
            bot.send_message(message.from_user.id, output_message)
        bot.send_message(message.from_user.id,
                         "Чтобы обновить информацию о вашем месте в списке поступающих, напишите команду /update")

    @bot.message_handler(commands=['update'])
    def get_update(message):
        bot.send_message(message.from_user.id, "Подождите пожалуйста. Бот обновляет данные и анализирует их")
        os.remove(f'{os.getcwd()}\\students.xlsx')
        parse_website_link(website_link)
        get_info(message)

    @bot.message_handler(commands=['commands'])
    def show_all_commands(message):
        all_commands = '''
        Список всех команд:
        /start - запускает бота
        /show - последнюю сохранененную информацию еще раз
        /update - обновляет информацию и выводит её
        /commands - выводит список всех команд
        /stop - выключает бота'''
        bot.send_message(message.from_user.id, all_commands)

    @bot.message_handler(commands=['stop'])
    def stop_bot(message):
        global SNILS, autoupdate_interval, website_link, flag_autoupdate, flag_update_interval, flag_SNILS
        SNILS = None
        autoupdate_interval = None
        website_link = ''
        flag_autoupdate = False
        flag_update_interval = False
        flag_SNILS = False
        if os.path.exists(f"{os.getcwd()}\\students.xlsx"):
            os.remove(f'{os.getcwd()}\\students.xlsx')
        bot.send_message(message.from_user.id, "Данные успешно отчищены.")

    @bot.message_handler(func=lambda x: True)
    def welcome_message(message):
        bot.reply_to(message, 'Привет! Это парсер списка поступающих в ВШЭ. Чтобы начать, введите команду /start')

    bot.polling()


def parse_website_link(website_link):
    # website_link = 'https://docs.google.com/spreadsheets/d/11Wci2MHaXvGuokesyxOOcIh_JBT6wH78Zu64pxaPZp8/edit#gid=1109409760'
    path_downloads = fr"{os.path.expanduser('~')}\Downloads\students.xlsx"
    xpath_input_button = "/html/body/div[2]/div[4]/div[1]/div[1]/div[1]"
    xpath_download_button = "//*[@aria-label = 'Скачать d']"
    xpath_download_format_type = "//*[@aria-label='Microsoft Excel (XLSX) x']"

    browser = webdriver.Chrome()
    browser.get(website_link)
    browser.find_element(by=By.XPATH, value=xpath_input_button).click()
    browser.find_element(by=By.XPATH, value=xpath_download_button).click()
    browser.find_element(by=By.XPATH, value=xpath_download_format_type).click()
    while not os.path.exists(path_downloads):
        time.sleep(0.1)
    shutil.move(path_downloads, os.getcwd())


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
            only_me_df.loc[:, "my_place"] = "-1"
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
            only_me_df.loc[:, "my_place"] = my_number
    only_me_df.loc[:, "get_budget_place"] = desired_values
    only_me_dict = only_me_df.T.to_dict()
    only_me_dict = list(only_me_dict.values())
    return (only_me_dict)


def is_SNILS_exist():
    df = pd.read_excel('students.xlsx', sheet_name='Sheet1')
    if SNILS in set(df['СНИЛС'].to_list()):
        return True
    return False


if __name__ == '__main__':
    create_telegram_bot()
