# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

def price_to_int(price:str):
    if price:
        return int(price.replace(' ',''))
    return price

class LeruaparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(price_to_int), output_processor=TakeFirst())
    image_urls = scrapy.Field()
    _id = scrapy.Field()
    href = scrapy.Field()
    def_list_keys = scrapy.Field()
    def_list_values = scrapy.Field()
    info = scrapy.Field()

