__all__ = ['get_params_to_calculate', 'get_stats']


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