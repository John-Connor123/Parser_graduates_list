__all__ = ['get_telegram_graphs', 'create_telegram_bot', 'set_telegram_params_work', 'work_telegram_bot']

import telebot
from telebot import types


def functions_for_handle():
    def get_SNILS(message):
        pass


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
    def run(message):
        bot.reply_to(message, "Введите свой СНИЛС:")

    @bot.message_handler(func=lambda x: True)
    def echo_all(message):
        bot.send_message(message.from_user.id, 'Привет! Это парсер списка поступающих в ВШЭ. Чтобы начать, введите команду /start')

    return bot


def set_telegram_params_work(auto_update=False):
    '''
    Настраивает работу telegram-бота.
    :param auto_update: параметр равен True, если требуется автообновление данных.
    Для единичного показа статистики параметр должен равняться False.
    P.s. По умолчанию параметр равен False.
    :return: None
    '''
    pass


def work_telegram_bot():
    '''
    Функция, через которую осуществяется управление телеграмм ботом
    :return: None
    '''
    bot = create_telegram_bot()
    bot.polling()

work_telegram_bot()
