# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.exceptions import DropItem
class ScrapyAlibabaPipeline(object):

    # def open_spider(self, spider):
    #     self.file = open('items.json', 'w')

    # def close_spider(self, spider):
    #     self.file.close()

    def process_item(self, item, spider):
        if item['must_contain'].lower() in item['title'].lower():
            return item
        else:
            raise DropItem("Title Did not contain {}".format(item['must_contain']))

