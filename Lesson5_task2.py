from selenium import webdriver
import time
from pymongo import MongoClient
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import json


def update_insert_new(collection, info):
    collection.insert_one(info)


def find_by_id(collection, id_value):  # ищем документы в базе данных
    return True if collection.count_documents({'href': id_value}) > 0 else False


client = MongoClient('127.0.0.1', 27017)
db = client['db_goods']
dbgoods = db.hitsgoods

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
driver.get('https://www.mvideo.ru/')

first_link = driver.find_element_by_xpath(
    "//body[@class='home']/div[@class='wrapper']/div[@class='page-content']/div[@class='main-holder sel-main-holder']/div[10]/div[1]")
actions = ActionChains(driver)
actions.move_to_element(first_link)
actions.perform()
time.sleep(5)

while True:
    items = first_link.find_elements_by_tag_name('li')
    rel = ''
    for item in items:

        data_info = {}
        link = item.find_element_by_tag_name('a')
        href = link.get_attribute('href')
        rel = link.get_attribute('rel')

        if not find_by_id(dbgoods, href):
            datainit = json.loads(link.get_attribute('data-product-info'))
            data_info['rel'] = rel
            data_info['href'] = href
            data_info['data-product-info'] = datainit

            update_insert_new(dbgoods, data_info)

    try:
        button = first_link.find_element_by_xpath(".//a[@class='next-btn sel-hits-button-next']")
        button.click()
        time.sleep(0.5)
    except:
        print('finish')
        break
