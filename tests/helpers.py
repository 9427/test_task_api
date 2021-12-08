import random
import requests
import time

API_ROUTE = 'http://backend:5000/api/v1/employees'
DEFAULT_VALS = {
    'lastname': 'Pupkin',
    'firstname': 'Vasya',
    'patronym': 'Ivanovich',
    'birthyear': 1994,
    'id': 1234,
    'salary': 250000,
    'jobname': 'Senior Pomidor Developer',
    'company': 'RedApple',
    'department': 'Pomidor Team'
}


def create_query(query_vals):
    """ Создать запрос к API из словаря

    :param query_vals: словарь с аргументами
    """
    query = '?'
    for key in query_vals.keys():
        query = query + str(key) + '=' + str(query_vals[key]) + '&'
    return query[:-1]


def get(query, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param query: запрос с адресом
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    delay = 0
    query = API_ROUTE + query
    for i in range(max_retries):
        try:
            response = requests.get(query)
            return response.json()
        except:
            pass
        time.sleep(delay)
        delay = min(delay * backoff_factor, timeout)
        delay += random.random()
    return response