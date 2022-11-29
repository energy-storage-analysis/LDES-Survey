# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import os
from scrapy.exceptions import DropItem


class PriceListPipeline(object):

    def open_spider(self, spider):

        if not os.path.exists('output'): os.mkdir('output')

        #with the -a spider_iter=<num> kwarg the file can instead be output to output/temp to be combined later. 

        self.file = open('output/items_price_list.jl', 'w')
        self.dropfile = open('output/items_price_list_dropped.jl', 'w')

    def close_spider(self, spider):
        self.file.close()
        self.dropfile.close()

    def drop_item(self, item, message):
        item['drop_reason'] = message
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.dropfile.write(line)
        raise DropItem(message)

    def process_item(self, item, spider):

        
        if not item['manufacturer']:
            self.drop_item(item, "No Data")
        
        #All conditions met, write to file
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item


class ProductListPipeline(object):

    def open_spider(self, spider):

        if not os.path.exists('output'): os.mkdir('output')

        #with the -a spider_iter=<num> kwarg the file can instead be output to output/temp to be combined later. 

        self.file = open('output/items_product_list.jl', 'w')
        self.dropfile = open('output/items_product_list_dropped.jl', 'w')

    def close_spider(self, spider):
        self.file.close()
        self.dropfile.close()

    def drop_item(self, item, message):
        item['drop_reason'] = message
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.dropfile.write(line)
        raise DropItem(message)

    def process_item(self, item, spider):

        
        if not item['product']:
            self.drop_item(item, "No Data")
        
        #All conditions met, write to file
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item