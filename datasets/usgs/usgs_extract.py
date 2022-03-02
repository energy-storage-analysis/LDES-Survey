#%%
import os
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET

import sys
sys.path.append('..')

from pdf_utils import average_range

salient_dir = 'data/salient'

csv_fns = [f for f in os.listdir(salient_dir) if '.csv' in f]
csv_fps = [os.path.join(salient_dir, fn) for fn in csv_fns]

# %%
dfs = [pd.read_csv(fp) for fp in csv_fps]
len(dfs)
#%%

df = dfs[0]


#%%

dfs_all = []

for fp in csv_fps[:]:


    xml_path = fp.replace('salient.csv','meta.xml')


    tree = ET.parse(xml_path)

    root = tree.getroot()

    attr_labels = []
    attr_defs = []

    for attr in root.iter('attr'):
        attr_labels.append(attr[0].text.strip())
        attr_defs.append(attr[1].text.strip())

    s_attrs = pd.Series(attr_defs, index=attr_labels)
    s_attrs.index


    df = pd.read_csv(fp)

    if fp == 'data/salient\mcs2022-sulfu_salient.csv':
        df = df.rename(columns={'Price_Sulfur_dtdt': 'Price_Sulfur_dt'})

    price_cols = [col for col in df.columns if 'Price' in col]
    if len(price_cols):



        try:
            s_desc = s_attrs[price_cols]
        except KeyError:
            print(fp)
            continue

        dfs_prices = []
        for col in price_cols:
            df_temp = df[[col, 'Year','Commodity']]
            df_temp = df_temp.rename({col:'price'}, axis=1)
            df_temp['price_name'] = col.replace('Price_','').replace('_Price', '')
            # df_temp['price_name'] = df_temp['price_name'].str.removeprefix('_Price')

            df_temp['price_desc'] = s_attrs[col]
            dfs_prices.append(df_temp)

        df = pd.concat(dfs_prices) 


        dfs_all.append(df[['price', 'price_name','Commodity', 'Year', 'price_desc']])

    else:
        print("No price columns for {}".format(fp))

df_prices =  pd.concat(dfs_all).reset_index(drop=True)
df_prices




df_prices['price'] = df_prices['price'].astype(str).str.strip()
df_prices['price'] =   df_prices['price'].apply(average_range)

df_prices['price'] = df_prices['price'].str.replace("Variable, depending on type of product", "")
df_prices['price'] = df_prices['price'].replace('',np.nan).replace('XX',np.nan)
df_prices['price'].astype(float)

#%%

price_units = ['ctslb','dlb','dkg','kg','dt','dst','dlb','dct','Index', 't', 'df', 'dto', 'dtoz','dg']

units_regex = "|".join(price_units)
pat_1 = '^({})$'.format(units_regex)
pat_2 = '^({})_'.format(units_regex)
pat_3 = '_({})$'.format(units_regex)

price_units_1 = df_prices['price_name'].str.extract(pat_1).dropna()
df_prices['price_name'] = df_prices['price_name'].str.replace(pat_1,'', regex=True)

price_units_2 = df_prices['price_name'].str.extract(pat_2).dropna()
df_prices['price_name'] = df_prices['price_name'].str.replace(pat_2,'', regex=True)

price_units_3 = df_prices['price_name'].str.extract(pat_3).dropna()
df_prices['price_name'] = df_prices['price_name'].str.replace(pat_3,'', regex=True)
# price_units_2
#%%

price_units = pd.concat([price_units_1, price_units_2, price_units_3])
price_units

df_prices['price_units'] = price_units

#%%

#This range appears to be incorrectly labeled 'dt'
df_prices.loc[710:719]['price_units'] = 'dkg'

#%%


df_prices = df_prices[['Commodity','price','price_units','price_name','Year','price_desc']]

df_prices = df_prices.rename({
    'price_name': 'price_info'
}, axis=1)

df_prices.to_csv('output/prices.csv')
# %%

# %%