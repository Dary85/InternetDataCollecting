# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from pymongo import MongoClient
import re

class JobparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.books

    def process_item(self, item, spider):
        # name = item['name']
        if spider.name == 'Labirint':
             try:
                item['main_price'] = int(item['main_price'])
             except:
                print(f"Error to convert main_price {item['main_price'] }")

             item['name'] = item['name'][item['name'].find(':')+1:]

        elif spider.name == 'Book24':
            try:
                item['main_price'] = int(''.join(re.findall(r'\d',item['main_price'])))
            except:
                print(f"Error to convert main_price {item['main_price']}")
            item['author'] = ','.join(item['author'])
        try:
            item['discount_price'] = int(item['discount_price'])
        except:
            print(f"Error to convert discount_price {item['discount_price']}")

        collection = self.mongo_base[spider.name]
        collection.insert_one( item)

        return item
