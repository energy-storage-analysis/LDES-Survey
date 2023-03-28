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

import urllib.parse

START_ROW = 0
# NUM_ROWS = sys.maxsize
NUM_ROWS = 5

RESOURCE_FOLDER = os.path.join(os.path.dirname(__file__), "../resources")

def format_url(search_str):
    search_str = search_str.replace(" ", "+")
    search_str = urllib.parse.quote(search_str, safe="+")
    url = "https://dir.indiamart.com/search.mp?ss={}&mcatid=12450&catid=180&prdsrc=1&stype=attr=1".format(search_str)
    return url

class IndiamartCrawlerSpider(scrapy.Spider):
    name = 'indiamart_crawler'
    allowed_domains = ['indiamart.com']
    start_urls = ['http://indiamart.com/']
    extractor = Extractor.from_yaml_file(os.path.join(RESOURCE_FOLDER, "search_results.yml"))

    def start_requests(self):
        """Read keywords from keywords file amd construct the search URL"""

        df_search = pd.read_csv(os.path.join(RESOURCE_FOLDER, 'mat_data_searches.csv'), index_col=0)
        df_search = df_search.iloc[START_ROW:START_ROW + NUM_ROWS]
        df_search = df_search[['search_text', 'must_contain', 'split_hydrate']]
        df_search = df_search.dropna(subset=['search_text'])

        for idx, row in df_search.iterrows():
            search_text=row["search_text"]

            url = format_url(search_text)
            # The meta is used to send our search text into the parser as metadata
            meta_dict = {
            'index': idx,
            'search_text': search_text,
            'must_contain': row['must_contain'],
            'split_hydrate': row['split_hydrate']
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