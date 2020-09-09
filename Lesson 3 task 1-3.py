from typing import List
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re
from pymongo import MongoClient


def find_by_sallary(collection, more_then=0):  # ищем все вакансии с зп больше указанной
    for vacancy in collection.find({"$or": [{'SallaryMin': {"$gte": more_then}}, {'SallaryMin': {"$gte": more_then}}]}):
        pprint(vacancy)


def add_new(collection, serials):  # добавляем новую
    for serial in serials:
        result = list(collection.find({'link': serial['link']}).limit(1))
        if len(result) == 0:
            collection.insert_one(serial)


def update_insert_new(collection, serials):  # обновляем и добавляем,если не нашли
    for serial in serials:
        collection.update({'link': serial['link']}, serial, {'upsert': True})


def insert_all(collection, serials):  # обновляем и добавляем,если не нашли
    collection.insert_many(serials)


def collect_hh(**parameters):  # собираем данные с сайта HH.ru
    main_link = 'https://hh.ru/search/vacancy'
    serials = parameters['serials']
    i = 0
    while i <= parameters['page_till']:

        param = {'text': parameters['vacancy'],
                 'page': i}
        i += 1
        response = requests.get(main_link, headers=parameters['headers'], params=param)

        soup = bs(response.text, 'html.parser')

        serials_list = soup.find_all('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})

        for serial in serials_list:
            serial_data = {}
            serial_link = serial.find('a', {'class': 'bloko-link HH-LinkModifier'}).get('href')
            serial_name = serial.find('a').getText()
            serial_sallary_div = serial.find('div', {'class': 'vacancy-serp-item__sidebar'})
            min_value = None
            max_value = None
            currency = None
            serial_sallary_text = ''
            if not serial_sallary_div.find('span',
                                           {'class': 'bloko-section-header-3 bloko-section-header-3_lite'}) == None:
                serial_sallary_text = serial_sallary_div.find('span', {
                    'class': 'bloko-section-header-3 bloko-section-header-3_lite'}).getText()
                result1: List[str] = re.split(r'[-/xa\s]', serial_sallary_text)  # разбор строки с зп

                if result1[0] == 'от':
                    min_value = int(result1[1] + result1[2])
                    currency = result1[3]
                elif result1[0] == 'до':
                    max_value = int(result1[1] + result1[2])
                    currency = result1[3]
                elif len(re.findall(r'\d', result1[0])) > 0:
                    min_value = int(result1[0] + result1[1])
                    max_value = int(result1[2] + result1[3])
                    currency = result1[4]

            serial_data['name'] = serial_name
            serial_data['link'] = serial_link
            serial_data['sallary_text'] = serial_sallary_text
            serial_data['currency'] = currency
            serial_data['SallaryMin'] = min_value
            serial_data['SallaryMax'] = max_value
            serial_data['website'] = 'www.hh.ru'

            serials.append(serial_data)

        next_button = soup.find('a', class_='bloko-button HH-Pager-Controls-Next HH-Pager-Control')

        if next_button == None:
            break


# pprint(serials)

def collect_sj(**parameters):  # собираем данные с сайта sj.ru
    main_link = 'https://www.superjob.ru/vacancy/search/'

    serials = parameters['serials']
    i = 0
    while i <= parameters['page_till']:
        i = i + 1
        param = {'keywords': parameters['vacancy'],
                 'page': i}

        response = requests.get(main_link, headers=parameters['headers'], params=param)

        soup = bs(response.text, 'html.parser')

        serials_list = soup.find_all('div', {'class': 'iJCa5 f-test-vacancy-item _1fma_ undefined _2nteL'})

        for serial in serials_list:
            serial_data = {}
            serial_link = main_link + serial.find('a').get('href')
            serial_name = serial.find('a').getText()
            serial_sallary_text = serial.find('span',
                                              class_='_1OuF_ _1qw9T f-test-text-company-item-salary').text
            result1: List[str] = re.split(r'[/xa\s]', serial_sallary_text)  # разбор строки с зп
            min_value = None
            max_value = None
            currency = None

            if result1[0] == 'от':
                min_value = int(result1[1] + result1[2])
                currency = result1[3]
            elif result1[0] == 'до':
                max_value = int(result1[1] + result1[2])
                currency = result1[3]
            elif len(re.findall(r'\d', result1[0])) > 0 and result1[2] == '—':
                min_value = int(result1[0] + result1[1])
                max_value = int(result1[3] + result1[4])
                currency = result1[5]
            elif len(re.findall(r'\d', result1[0])) > 0 and not result1[2] == '—':
                min_value = int(result1[0] + result1[1])
                max_value = int(result1[0] + result1[1])
                currency = result1[2]

            serial_data['name'] = serial_name
            serial_data['link'] = serial_link
            serial_data['sallary_text'] = serial_sallary_text
            serial_data['currency'] = currency
            serial_data['SallaryMin'] = min_value
            serial_data['SallaryMax'] = max_value
            serial_data['website'] = 'www.superjob.ru'

            serials.append(serial_data)

        next_button = soup.find('a',
                                {'rel': 'next', 'class': 'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe'})

        if next_button == None:
            break


# pprint(serials)

# собираем данные с сайтов

vacancy = input('Enter vacancy name: ')
page_till = int(input('Enter number of pages'))

vacancy.replace(' ', '+')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/85.0.4183.83 Safari/537.36'}

serials = []

collect_hh(page_till=page_till, serials=serials, headers=headers, vacancy=vacancy)
collect_sj(page_till=page_till, serials=serials, headers=headers, vacancy=vacancy)

# pprint(serials)
while True:
    add = input("Add or update (enter a to add ot u to update): ")

    if not (add == 'a' or add == 'u'):
        print('Wrong answer, tru again ')
        continue
    else:
        # подключаемся к базе
        client = MongoClient('127.0.0.1', 27017)
        db = client['db_vacancies']

        vac = db.vacancies

        if add == 'a':
            # добавляем найденные вакансии

            insert_all(vac, serials)
            print(vac.count_documents({}))
        else:
            # Добавляем новые элементы если не найдены
            add_new(vac, serials)
            print(vac.count_documents({}))
        break

# ищем все что больше заданной суммы
amount = int(input('Enter sallary: '))
find_by_sallary(vac, amount)

# vac.delete_many({})
