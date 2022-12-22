# -*- coding: utf-8 -*-
import scrapy
import os
from selectorlib import Extractor
import sys
import pandas as pd
import re

START_ROW = 1
NUM_ROWS = sys.maxsize
# NUM_ROWS = 3

RESOURCE_FOLDER = os.path.join(os.path.dirname(__file__), "../resources")


class ChemBookPriceSpider(scrapy.Spider):
    name = 'cb_price_spider'
    allowed_domains = ['chemicalbook.com']
    start_urls = ['http://www.chemicalbook.com']
    extractor = Extractor.from_yaml_file(os.path.join(RESOURCE_FOLDER, "chemicalbook_price_list.yml"))

    custom_settings = {
        'ITEM_PIPELINES': {
            'chemical_book.pipelines.PriceListPipeline': 400
        }
    }

    def start_requests(self):
        """Read keywords from keywords file amd construct the search URL"""

        df_search = pd.read_csv(os.path.join(RESOURCE_FOLDER, 'cb_info.csv'), index_col=0)
        df_search = df_search.dropna(subset=['CBNumber'])
        df_search = df_search.iloc[START_ROW:START_ROW + NUM_ROWS]
        df_search = df_search[['CBNumber']]

        for idx, row in df_search.iterrows():
            cbn=row["CBNumber"]

            url="https://www.chemicalbook.com/SupplierPriceList_EN.aspx?cbn={}&page=1#price".format(
                cbn)
            # The meta is used to send our search text into the parser as metadata
            meta_dict = {
            'index': idx,
            'cbn': cbn
            }

            yield scrapy.Request(url, callback = self.parse_amounts, meta = meta_dict, cb_kwargs=meta_dict)


    def parse_amounts(self, response, **meta_dict):
        data = self.extractor.extract(response.text,base_url=response.url)

        amounts = data['package_selector_list']

        if amounts != None:
            amounts = amounts.split(" ")
            keep_amounts = ['kg','lb']

            amounts_keep = []
            for amount_str in amounts:
                if any([s in amount_str.lower() for s in keep_amounts]):
                    amounts_keep.append(amount_str)

            amounts_url_str = "%7C".join(amounts_keep)
            cbn = meta_dict['cbn']

            new_url = "https://www.chemicalbook.com/SupplierPriceList_EN.aspx?cbn={}&c={}".format(
                    cbn, amounts_url_str)

            yield scrapy.Request(new_url, callback = self.parse_downselected_table, meta = meta_dict, cb_kwargs=meta_dict)

    def parse_downselected_table(self, response, **meta_dict):

        data = self.extractor.extract(response.text,base_url=response.url)
        data.update(meta_dict)
        yield data