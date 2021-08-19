from collections import defaultdict, OrderedDict
import operator


def get_rating(list_of_ip):
    """
    Функция принимает список IP-адресов из лог-файла access.log, с которых совершались запросы на сервер.
    Возвращает словарь вида {"IP-адрес": количество вхождений в список (==количество запросов)}

    """
    origin_ip_list = list(set(list_of_ip))
    rating = dict()
    for i in origin_ip_list:
        rating.update({i:list_of_ip.count(i)})
    return rating


def sort_ip_dict(dictionary:dict, display=-1, reversed=True):
    """
    :param dictionary: словарь, который требуется отсортировать по значениям ключа
    :param display: количество пар "Ключ:Значение", которые нужно будет сохранить в отсортированом словаре
                    Значение -1 (по умолчанию): для вывода всех пар Ключ:Значение" переданного словаря
    :param reversed: сортировать по возрастанию (reversed = False) или по убыванию (reversed=True) Значения
    :return: отсортированный по значениям объект OrderDict

    """
    sorted_dict = OrderedDict()
    sorted_tuples = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=reversed)
    displayed_val = 0
    for k, v in sorted_tuples:
        if displayed_val == display:
            break
        sorted_dict[k] = v
        displayed_val +=1
    return sorted_dict