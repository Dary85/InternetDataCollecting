from pprint import pprint
from lxml import html
import requests
import datetime as dt
from dateutil.parser import parse


def news_mail(**parameters):
    main_link = 'https://news.mail.ru'
    response = requests.get(main_link, headers=parameters['headers'])

    dom = html.fromstring(response.text)

    items = dom.xpath(
        "//span[@class ='photo__title photo__title_new photo__title_new_hidden js-topnews__notification']")  # Основные новости
    mail_news = parameters['news']
    for item in items:
        news_descr = {}
        ref = item.xpath(".//../../@href")
        title = item.xpath(".//text()")
        date = []
        source = []
        if len(ref) > 0:
            res_details = requests.get(main_link + ref[0], headers=parameters['headers'])
            res_dom = html.fromstring(res_details.text)
            details = res_dom.xpath("//div [@class = 'breadcrumbs breadcrumbs_article js-ago-wrapper']")
            for detail in details:
                date = detail.xpath(".//span[@class='note__text breadcrumbs__text js-ago']/@datetime")
                source = detail.xpath(".//a[@class='link color_gray breadcrumbs__link']/@href")
                date = parse(date[0]).date().strftime("%Y-%m-%d") if len(date) > 0 else None

        news_descr['title'] = title[0].replace('\xa0', '') if len(title) > 0 else ''
        news_descr['ref'] = main_link + ref[0] if len(ref) > 0 else ''
        news_descr['date'] = date
        news_descr['source'] = source[0] if len(source) > 0 else ''
        mail_news.append(news_descr)


def news_yandex(**parameters):
    main_link = 'https://yandex.ru/news/'
    response = requests.get(main_link, headers=parameters['headers'])

    dom = html.fromstring(response.text)

    items = dom.xpath(
        "//div[contains(@class,'mg-grid__col mg-grid__col_xs')]//article[contains(@class,'mg-card news-card news-card')]")
    ya_news = parameters['news']
    for item in items:
        news_descr = {}
        ref = item.xpath(".//..//a[@class='news-card__link']/@href")
        title = item.xpath(".//a[@class='news-card__link']//h2[@class='news-card__title']//text()")

        source = item.xpath(".//span[@class='mg-card-source__source']//a//text()")
        date = item.xpath(".//span[@class='mg-card-source__time']/text()")

        if len(date) > 0:
            dtoday = dt.datetime.now()
            yesterday = dtoday - dt.timedelta(days=1)
            date = dtoday.date().strftime("%Y-%m-%d") if date[0].find('вчера') > -1 else yesterday.date().strftime(
                "%Y-%m-%d")

        news_descr['title'] = title[0].replace('\xa0', '') if len(title) > 0 else ''
        news_descr['ref'] = ref[0] if len(ref) > 0 else ''
        news_descr['date'] = date
        news_descr['source'] = source[0] if len(source) > 0 else ''
        ya_news.append(news_descr)


def news_lenta(**parameters):
    main_link = 'https://lenta.ru/'
    response = requests.get(main_link, headers=parameters['headers'])

    dom = html.fromstring(response.text)

    items = dom.xpath("//section[@class='row b-top7-for-main js-top-seven']")
    lenta_news = parameters['news']

    for item in items:
        for detail in item.xpath(".//a[@href]//time[@class='g-time']"):
            news_descr = {}
            ref = detail.xpath(".//../@href")
            title = detail.xpath(".//..//text()")

            source = 'lenta.ru'
            date = detail.xpath(".//@title")[0] if len(detail.xpath(".//@title")) > 0 else None

            news_descr['title'] = title[1].replace('\xa0', '') if len(title) > 1 else ''
            news_descr['ref'] = main_link + ref[0] if len(ref) > 0 else ''
            news_descr['date'] = date
            news_descr['source'] = source
            lenta_news.append(news_descr)


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/85.0.4183.83 Safari/537.36'}

news = []

try:
    news_mail(headers=headers, news=news)
except:
    pprint('mail')
news_yandex(headers=headers, news=news)
news_lenta(headers=headers, news=news)
pprint(news)
