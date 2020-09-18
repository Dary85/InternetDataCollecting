from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from pymongo import MongoClient
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


def update_insert_new(collection, info): # вставим новый элемент в базу
    collection.insert_one(info)


def find_by_id(collection, id_value):  # ищем документы в базе данных
    return True if collection.count_documents({'data_id': id_value}) > 0 else False


def collect_info(**param):  # соберем данные по письмам

    linkmail = param['linkmail']
    driver = param['driver']
    collection = param['collection']

    mails_descr = {}

    href = linkmail.get_attribute('href')
    data_id = linkmail.get_attribute('data-id')

    from_mail = linkmail.find_element_by_class_name('ll-crpt').get_attribute('title')
    date = linkmail.find_element_by_class_name('llc__item_date').get_attribute('title')

    linkmail.click()
    time.sleep(4)

    try:
        mail_title = driver.find_element_by_xpath("//h2[@class='thread__subject']").text
    except:
        mail_title = ''
        print(f'Не нашел заголовок для {href}')
    try:
        mail_content = driver.find_element_by_class_name('letter-body__body-content').text

    except:
        mail_content = ''
        print(f'Не нашел тело письма для {href}')

    try:
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(2)
    except:
        print("Error NoSuchElementException")

    mails_descr['href'] = href
    mails_descr['data_id'] = data_id
    mails_descr['from_mail'] = from_mail
    mails_descr['date'] = date
    mails_descr['mail_title'] = mail_title
    mails_descr['mail_content'] = mail_content

    update_insert_new(collection, mails_descr)

    param['emails'].append(mails_descr)

#подключаемся к базе монго
client = MongoClient('127.0.0.1', 27017)
db = client['db_mail']
dbemails = db.emails

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome('chromedriver.exe',options=chrome_options)
driver.get('https://mail.ru/')

#войдем в ящик
login = driver.find_element_by_id('mailbox:login-input')
login.send_keys('study.ai_172@mail.ru')

buttonpsw = driver.find_element_by_id('mailbox:submit-button')
buttonpsw.click()

passw = driver.find_element_by_id('mailbox:password-input')
passw.send_keys('NextPassword172')
passw.send_keys(Keys.RETURN)

emails = []

time.sleep(2) #ждем пока страница загрузится

LastValue = None

while True:

    time.sleep(3)

    linkmails = driver.find_elements_by_class_name('js-letter-list-item')

    if LastValue == linkmails[-1]:
        break

    actions = ActionChains(driver)
    actions.move_to_element(linkmails[-1])
    actions.perform()

    LastValue = linkmails[-1]

    for linkmail in linkmails:

        try:
            data_id = linkmail.get_attribute('data-id')
        except:
            continue

        if not find_by_id(dbemails, data_id):
            collect_info(emails=emails, linkmail=linkmail, driver=driver, collection=dbemails)