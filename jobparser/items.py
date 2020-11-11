# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:

    name = scrapy.Field()
    author = scrapy.Field()
    main_price = scrapy.Field()
    discount_price = scrapy.Field()
    rating = scrapy.Field()
    href = scrapy.Field()
    _id = scrapy.Field()

