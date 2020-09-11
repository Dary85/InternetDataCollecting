from typing import List

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re



main_link = 'https://www.superjob.ru/vacancy/search/'

vacancy = input('Enter vacancy name: ')
page_till = int(input('Enter number of pages'))

vacancy.replace(' ', '+')

headers = {'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/85.0.4183.83 Safari/537.36'}
serials = []
i = 0
while i <= page_till:
    i = i+1
    param = {'keywords': vacancy,
         'page': i}

    response = requests.get(main_link, headers=headers, params=param)

    soup = bs(response.text, 'html.parser')

    serials_list = soup.find_all('div', {'class': 'iJCa5 f-test-vacancy-item _1fma_ undefined _2nteL'})


    for serial in serials_list:
        serial_data = {}
        serial_link = main_link + serial.find('a').get('href')
        serial_name = serial.find('a').getText()
        serial_sallary_text = serial.find('span',
                                 class_='_1OuF_ _1qw9T f-test-text-company-item-salary').text
        result1: List[str] = re.split(r'[/xa\s]', serial_sallary_text)
        min_value = None
        max_value = None
        currency = None

        if result1[0] == 'от':
            min_value = int(result1[1]+result1[2])
            currency = result1[3]
        elif result1[0] == 'до':
            max_value = int(result1[1] + result1[2])
            currency = result1[3]
        elif len(re.findall(r'\d', result1[0]))> 0 and  result1[2]=='—':
            min_value = int(result1[0]+result1[1])
            max_value = int(result1[3]+result1[4])
            currency = result1[5]
        elif len(re.findall(r'\d', result1[0]))> 0 and not result1[2]=='—':
            min_value = int(result1[0]+result1[1])
            max_value = int(result1[0]+result1[1])
            currency = result1[2]


        serial_data['name'] = serial_name
        serial_data['link'] = serial_link
        serial_data['sallary_text'] = serial_sallary_text
        serial_data['currency'] = currency
        serial_data['SallaryMin'] = min_value
        serial_data['SallaryMax'] = max_value
        serial_data['website'] = 'www.superjob.ru'

        serials.append(serial_data)


pprint(serials)
