#!/usr/bin/env python
'''
Получение данных

На сайте портала открытых данных Москвы есть таблица с популярными именами
новорожденных. Напишите функцию, которая получает данные при помощи requests
и читает содержимое в формате json. Для получения данных используйте ссылку
http://api.data.mos.ru/v1/datasets/2009/rows

https://data.mos.ru/opendata/7704111479-svedeniya-o-naibolee-populyarnyh-jenskih-imenah-sredi-novorojdennyh
'''
import requests

from mos_api_key import mos_api_key


def get_names(url, print_result=None):
    ''' Загружает и возвращает имена. '''
    requests_params = {'api_key': mos_api_key}
    requests_timeout = (5, 30)
    try:
        names = requests.get(
            url,
            timeout=requests_timeout,
            params=requests_params)
        names.raise_for_status()
    except requests.exceptions.HTTPError as requests_exception:
        print('HTTP error: {}'.format(requests_exception))
        return 1
    except requests.exceptions.RequestException as requests_exception:
        print('Connection eror: {}'.format(requests_exception))
        return 2

    names_json = names.json()

    if not print_result == 'print_result':
        return names_json
    return '\nSuccesfully loaded names from {}.\nLength: {} lines.\nLines look\
 like this:\n{}'.format(url, len(names_json), names_json[0])


if __name__ == '__main__':
    print('\nЖенские имена',
          get_names('https://apidata.mos.ru/v1/datasets/2009/rows',
                    'print_result'))
    print('\nМужские имена',
          get_names('https://apidata.mos.ru/v1/datasets/2011/rows',
                    'print_result'))
