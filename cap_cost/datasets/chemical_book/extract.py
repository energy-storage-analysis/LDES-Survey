#%%

import os
import numpy as np
import pandas as pd
import pint

df = pd.read_json('output/items_price_list.jl', lines=True).set_index('index')

df = df[['manufacturer', 'packaging','price']]

dfs_new = []
for col in df.columns:
    dfe = df[col].explode()
    dfs_new.append(dfe)

df = pd.concat(dfs_new, axis=1)

df = df.where(~df['packaging'].str.contains('x')).dropna(how='all')
df = df.where(~df['packaging'].str.contains('X')).dropna(how='all')

df[['empty', 'amount', 'unit']] = df['packaging'].str.split(r'([\d\.]+)', expand=True)

df = df.drop('empty',axis=1)
df = df.drop('packaging',axis=1)
df['price'] = df['price'].str.strip('$')

df['price'] = df['price'].astype(float)
df['amount'] = df['amount'].astype(float)
df

#%%

units_keep = ['g','kg','lb']

df['unit'] = df['unit'].str.lower()

df = df.where(df['unit'].isin(units_keep)).dropna(how='all')

df


#%%



ureg = pint.UnitRegistry()

min_quantity_kg = []
min_unit_kg = []
for index, row in df.iterrows():
    unit = row['unit']
    amount = row['amount']

    val_min_unit = ureg.Quantity(row['amount'], '{}'.format(unit))
    min_quantity_kg.append(val_min_unit.to('kg').magnitude)

    # break

df['min_quantity_kg'] = min_quantity_kg
df['specific_price'] = df['price']/df['min_quantity_kg']

#%%


df = df.sort_index()

df.to_csv('output/extracted.csv')
