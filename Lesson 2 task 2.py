from typing import List

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re

main_link = 'https://hh.ru/search/vacancy'

vacancy = input('Enter vacancy name: ')
page_till = int(input('Enter number of pages'))

vacancy.replace(' ', '+')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/85.0.4183.83 Safari/537.36'}

serials = []
i = 0
while i <= page_till:

    param = {'text': vacancy,
             'page': i}
    i += 1
    response = requests.get(main_link, headers=headers, params=param)

    soup = bs(response.text, 'html.parser')



    serials_list = soup.find_all('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})

    for serial in serials_list:
        serial_data = {}
        serial_link = serial.find('a',{'class':'bloko-link HH-LinkModifier'}).get('href')
        serial_name = serial.find('a').getText()
        serial_sallary_div = serial.find('div',{'class':'vacancy-serp-item__sidebar'})
        min_value = None
        max_value = None
        currency = None
        serial_sallary_text = ''
        if not serial_sallary_div.find('span', {'class': 'bloko-section-header-3 bloko-section-header-3_lite'}) == None:
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
pprint(serials)

