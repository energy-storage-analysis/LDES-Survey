# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import csv
import os
from selectorlib import Extractor
import re 
import itertools
import sys
import pandas as pd

START_ROW = 0
NUM_ROWS = 5 #sys.maxsize

RESOURCE_FOLDER = os.path.join(os.path.dirname(__file__), "../resources")

class AlibabaCrawlerSpider(scrapy.Spider):
    name = 'alibaba_crawler'
    allowed_domains = ['alibaba.com']
    start_urls = ['http://alibaba.com/']
    extractor = Extractor.from_yaml_file(os.path.join(RESOURCE_FOLDER, "search_results.yml"))

    def start_requests(self):
        """Read keywords from keywords file amd construct the search URL"""

        df_search = pd.read_csv(os.path.join(RESOURCE_FOLDER, 'mat_data_searches.csv'), index_col=0)
        df_search = df_search.iloc[START_ROW:START_ROW + NUM_ROWS]
        df_search = df_search[['search_text', 'must_contain']]
        df_search = df_search.dropna(subset=['search_text'])

        for idx, row in df_search.iterrows():
            search_text=row["search_text"]

            url="https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText={0}&viewtype=G".format(
                search_text)
            # The meta is used to send our search text into the parser as metadata
            meta_dict = {
            'index': idx,
            'search_text': search_text,
            'must_contain': row['must_contain']
            }

            yield scrapy.Request(url, callback = self.parse, meta = meta_dict, cb_kwargs=meta_dict)


    def parse(self, response, **meta_dict):
        data = self.extractor.extract(response.text,base_url=response.url)
        if data['products']:
            for product in data['products']:
                outdict = {}
                outdict.update(meta_dict)
                outdict.update(product)
                yield outdict