# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter

class ScrapyAlibabaPipeline(object):

    def open_spider(self, spider):

        if not os.path.exists('output'): os.mkdir('output')
        self.file = open('output/items.jl', 'w')
        self.dropfile = open('output/items_dropped.jl', 'w')

    def close_spider(self, spider):
        self.file.close()
        self.dropfile.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"

        if not item['price']: 
            self.dropfile.write(line)
            raise DropItem("Missing Price")

        if item['must_contain'] == item['must_contain']:
            must_contain_strs = [s.strip().lower() for s in item['must_contain'].split(',')]
            contain_conditions = [s in item['title'].lower() for s in must_contain_strs]
            if not any(contain_conditions):
                self.dropfile.write(line)
                raise DropItem("Title Did not contain {}".format(item['must_contain']))

        if not item['min_order']:
            self.dropfile.write(line)
            raise DropItem("Missing Minimum Order")

        if 'piece' in item['min_order'].lower():
            self.dropfile.write(line)
            raise DropItem("'piece' found in Minimum Order ")

        #All conditions met, write to file
        self.file.write(line)
        return item

