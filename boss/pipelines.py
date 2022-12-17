# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class BossPipeline:
    def process_item(self, item, spider):
        host = 'localhost'
        port = 27017
        db_name = 'boss'
        client = pymongo.MongoClient(host=host, port=port)
        db = client[db_name]
        collection = db['job']
        collection.insert_one(dict(item))
        return item

