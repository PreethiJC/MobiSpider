# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

class PmPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def open_spider(self, spider):
        self.file = open("items.jl", 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.collection.replace_one(dict(item), dict(item), True)
        return item
