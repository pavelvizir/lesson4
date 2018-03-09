#!/usr/bin/env python
'''
1.  Вывод данных на сайте

    Добавьте на сайт страницу /names, на которой в табличном виде выведите
    данные об именах новорожденных, получаемые при помощи функции из
    предыдущей задачи. Пример простейшего оформления таблицы:
    <table>
        <tr>
            <th>Заголовок колонки 1</th>
        </tr>
        <tr>
            <td>Данные 1</td>
        </tr>
    </table>

2.  Фильтрация данных

    Ограничьте выводимые данные одним годом. Год должен указываться в URL
    как параметр, например /names?year=2016.

'''

from time import time
from flask import Flask, request
from get_names import get_names

app = Flask(__name__)


@app.route('/names')
def show_names():
    ''' Выводит в табличном виде данные об именах. '''
    global names
    global names_timestamp
    current_time = time()
    if not names or current_time - names_timestamp > cache_timeout:
        print('Downloading data.')
        names = get_names('https://apidata.mos.ru/v1/datasets/2009/rows')
        names_timestamp = time()
    else:
        print('Using cached data.')
    available_years = []
    for row in names:
        if row['Cells']['Year'] not in available_years:
            available_years.append(row['Cells']['Year'])

    year_arg = request.args.get('year')
    if year_arg:
        try:
            year = int(str(year_arg))
            if year not in available_years:
                return '<b>За %s год информации нет.</b>' % year
        except ValueError:
            return '<b>Год следует указывать числом!</b>'
    else:
        year = None
    result = ['<table>']
    if year:
        result.append('<caption><b>За ' + str(year) + ' год:</b></caption>')
        result.extend(['<tr>', '<th>Month</th>', '<th>Name</th>',
                       '<th>NumberOfPersons</th>', '</tr>'])
        for row in names:
            if row['Cells']['Year'] == year:
                result.extend([
                    '<tr>',
                    '<td>' + row['Cells']['Month'] + '</td>',
                    '<td>' + row['Cells']['Name'] + '</td>',
                    '<td>' + str(row['Cells']['NumberOfPersons']) + '</td>',
                    '</tr>'])
    else:
        result.append('<caption><b>За все годы:</b></caption>')
        result.extend(['<tr>', '<th>Year</th>', '<th>Month</th>',
                       '<th>Name</th>', '<th>NumberOfPersons</th>', '</tr>'])
        for row in names:
            result.extend([
                '<tr>',
                '<td>' + str(row['Cells']['Year']) + '</td>',
                '<td>' + row['Cells']['Month'] + '</td>',
                '<td>' + row['Cells']['Name'] + '</td>',
                '<td>' + str(row['Cells']['NumberOfPersons']) + '</td>',
                '</tr>'])
    result.append('</table>')
    return '\n'.join(result)


if __name__ == '__main__':
    cache_timeout = 300
    names = []
    names_timestamp = time()
    app.run()
