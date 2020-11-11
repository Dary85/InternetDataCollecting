# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
import re

class LeruaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.lerua_photo

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item



class LeruaPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
       if item['image_urls']:
           for img in item['image_urls']:
                try:
                    yield scrapy.Request(img.replace('w_82,h_82','w_1200,h_1200'))
                except Exception as e:
                    print(e)

    # def file_path(self, request, response=None, info=None):
    #    return 0
    def process_defenitions(self, def_list_keys,def_list_values,info_item):
        for i in range(len(def_list_keys)):
            info_item[def_list_keys[i]] = ' '.join(str_item.strip() for str_item in re.split(r'[ \n\s]',def_list_values[i]))

    def item_completed(self, results, item, info):
        if results:
            item['image_urls'] = [itm[1] for itm in results if itm[0]]
            item['info'] = {}
            self.process_defenitions(item['def_list_keys'], item['def_list_values'], item['info'])

        return item