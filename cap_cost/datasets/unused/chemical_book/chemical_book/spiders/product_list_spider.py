# -*- coding: utf-8 -*-
import scrapy
import os
from selectorlib import Extractor
import sys
import pandas as pd

START_ROW = 1
NUM_ROWS = sys.maxsize
# NUM_ROWS = 3

RESOURCE_FOLDER = os.path.join(os.path.dirname(__file__), "../resources")



class ChemBookPriceSpider(scrapy.Spider):
    name = 'cb_product_list'
    allowed_domains = ['chemicalbook.com']
    start_urls = ['http://www.chemicalbook.com']
    extractor = Extractor.from_yaml_file(os.path.join(RESOURCE_FOLDER, "chemicalbook_product_list.yml"))

    custom_settings = {
        'ITEM_PIPELINES': {
            'chemical_book.pipelines.ProductListPipeline': 400
        }
    }

    def start_requests(self):
        """Read keywords from keywords file amd construct the search URL"""

        df_search = pd.read_csv(os.path.join(RESOURCE_FOLDER, 'cb_info.csv'), index_col=0)
        df_search = df_search.iloc[START_ROW:START_ROW + NUM_ROWS]
        df_search = df_search[['CBNumber']]
        df_search = df_search.dropna(subset=['CBNumber'])

        for idx, row in df_search.iterrows():
            cbn=row["CBNumber"]

            url="https://www.chemicalbook.com/ProductList_En.aspx?kwd={}&hp=true&c=1KG%7C2kg%7C2.5Kg%7C5KG%7C10kg%7C25KG%7C50kg%7C1lb%7C1%20kg%7C2.5%20KG%7C5%20Lb".format(
                cbn)
            # The meta is used to send our search text into the parser as metadata
            meta_dict = {
            'index': idx,
            }

            yield scrapy.Request(url, callback = self.parse, meta = meta_dict, cb_kwargs=meta_dict)


    def parse(self, response, **meta_dict):
        data = self.extractor.extract(response.text,base_url=response.url)
        data.update(meta_dict)
        yield data