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
#%%

cols_not_price = [col for col in df.columns if col != 'price']

df = pd.concat([
df[cols_not_price].groupby('original_name').first().drop('year',axis=1),
df[['original_name','price']].groupby('original_name').mean()
], axis=1)
df


#%%
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


specific_price = []
for index, row in df.iterrows():
    unit = row['price_units']
    val = row['price']
    val = ureg.Quantity(val, unit)
    val = val.to('USD/kg').magnitude
    specific_price.append(val)

df['specific_price'] = specific_price

#%%



from es_utils.chem import process_chem_lookup

chem_lookup = pd.read_csv('chem_lookup.csv')
chem_lookup = process_chem_lookup(chem_lookup)
df = pd.merge(df, chem_lookup, on='original_name')
# df = df.drop('original_name', axis=1)

#Grouping by the orignal name above, can keep a lot of the original data (this basically averages over years)
df.to_csv('output/processed_orig.csv', index=False)

#%%


#%%
df_combine = df.groupby('index')[['specific_price']].mean()

from es_utils import join_col_vals
df_combine['original_name']= df.groupby('index')['original_name'].apply(join_col_vals)

df_combine['molecular_formula']= df.groupby('index')['molecular_formula'].apply(join_col_vals)

from es_utils import extract_df_mat
df_price = extract_df_mat(df_combine)
df_price.to_csv('output/mat_data.csv')
