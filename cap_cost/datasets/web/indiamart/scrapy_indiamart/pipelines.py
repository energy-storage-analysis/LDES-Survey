# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter

class ScrapyIndiamartPipeline(object):

    def open_spider(self, spider):

        if not os.path.exists('scraped_data'): os.mkdir('scraped_data')
        if not os.path.exists('scraped_data/temp'): os.mkdir('scraped_data/temp')
        
        #with the -a spider_iter=<num> kwarg the file can instead be scraped_data to scraped_data/temp to be combined later. 
        if hasattr(spider, 'spider_iter'):
            i = spider.spider_iter
            self.file = open('scraped_data/temp/items_{}.jl'.format(i), 'w')
            self.dropfile = open('scraped_data/temp/items_dropped_{}.jl'.format(i), 'w')
        else:
            self.file = open('scraped_data/items.jl', 'w')
            self.dropfile = open('scraped_data/items_dropped.jl', 'w')

    def close_spider(self, spider):
        self.file.close()
        self.dropfile.close()

    def drop_item(self, item, message):
        item['drop_reason'] = message
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.dropfile.write(line)
        raise DropItem(message)

    def process_item(self, item, spider):
        
        # #TODO: figure out price_normal and price_promotion (see css selctors). I think this will be fixed if we just follow the response to the product page, vs trying to pull the price from the search results.
        # if not item['price_normal'] and not item['price_promotion']: 
        #     self.drop_item(item, "Missing Price")

        if item['must_contain'] == item['must_contain']:
            must_contain_strs = [s.strip().lower() for s in item['must_contain'].split(',')]
            contain_conditions = [s in item['title'].lower() for s in must_contain_strs]
            if not any(contain_conditions):
                self.drop_item(item,"Title Did not contain {}".format(item['must_contain']))

        # if not item['min_order']:
        #     self.drop_item(item, "Missing Minimum Order")
        if not item['price_amount']:
            self.drop_item(item, "Missing Price Amount")

        for s in ['piece','unit']:
            if s in item['price_amount'].lower():
                self.drop_item(item,"{} found in price amount".format(s))

        if 'ask price' in item['price'].lower():
            self.drop_item(item,"Ask Price" )

        #All conditions met, write to file
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item

