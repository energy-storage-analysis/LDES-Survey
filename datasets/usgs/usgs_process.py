#%%

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import pint
ureg = pint.UnitRegistry()
ureg.load_definitions('unit_defs.txt')



# %%
df = pd.read_csv('output/extracted.csv', index_col=0)
df = df.dropna(subset=['price'])
df

df = df.where(df['price_units'] != 'Index').dropna(subset=['price_units']) #TODO: how to deal with consumer price index

df['price_units'] = df['price_units'].replace({
    'ctslb': 'cents/lb',
    'dt': 'USD/ton',
    'dkg' : 'USD/kg',
    'dg': 'USD/g',
    'dlb':'USD/lb',
    'dto':'USD/ton',
    't':'USD/ton',
    'dct':'USD/carat',
    'dtoz':'USD/toz',
    'dst': 'USD/short_ton',
    'df':'USD/flask',
    'kg': 'USD/kg'
})

df['price_units'].value_counts()


price_per_kg = []
for index, row in df.iterrows():
    unit = row['price_units']
    val = row['price']
    val = ureg.Quantity(val, unit)
    val = val.to('USD/kg').magnitude
    price_per_kg.append(val)

df['price_per_kg'] = price_per_kg

#%%

chem_lookup = pd.read_csv('output/chem_lookup.csv', index_col=0)
chem_lookup
#%%

chemical_names = chem_lookup.loc[df['full_name'].values]
df['chemical'] = chemical_names.values


df = df.drop('full_name', axis=1)
#%%

df = df[['Commodity', 'price_info', 'chemical', 'price', 'price_units', 'Year', 'price_desc', 'price_per_kg']]

df.to_csv('output/processed.csv')
# %%
