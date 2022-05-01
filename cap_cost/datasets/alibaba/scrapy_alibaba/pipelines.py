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


        #with the -a spider_iter=<num> kwarg the file can instead be output to output/temp to be combined later. 
        if hasattr(spider, 'spider_iter'):
            i = spider.spider_iter
            self.file = open('output/temp/items_{}.jl'.format(i), 'w')
            self.dropfile = open('output/temp/items_dropped_{}.jl'.format(i), 'w')
        else:
            self.file = open('output/items.jl', 'w')
            self.dropfile = open('output/items_dropped.jl', 'w')

    def close_spider(self, spider):
        self.file.close()
        self.dropfile.close()

    def drop_item(self, item, message):
        item['drop_reason'] = message
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.dropfile.write(line)
        raise DropItem(message)

    def process_item(self, item, spider):

        if not item['price_normal'] and not item['price_promotion']: 
            self.drop_item(item, "Missing Price")

        if item['must_contain'] == item['must_contain']:
            must_contain_strs = [s.strip().lower() for s in item['must_contain'].split(',')]
            contain_conditions = [s in item['title'].lower() for s in must_contain_strs]
            if not any(contain_conditions):
                self.drop_item(item,"Title Did not contain {}".format(item['must_contain']))

        if not item['min_order']:
            self.drop_item(item, "Missing Minimum Order")

        if 'piece' in item['min_order'].lower():
            self.drop_item(item,"'piece' found in Minimum Order " )

        #All conditions met, write to file
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item

