__all__ = ['get_telegram_graphs', 'create_telegram_bot', 'set_telegram_params_work', 'work_telegram_bot']


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
    :return: токен телеграмм бота
    '''
    pass


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
    pass