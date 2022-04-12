#%%
import os
import numpy as np
import pandas as pd


df = pd.read_csv('extracted/extracted.csv')

df = df.rename({
    'Name': 'original_name',
    'Avg With Rate': 'price',
    'Unit': 'mass_unit'
},axis=1)


import pint

ureg = pint.UnitRegistry()
ureg.load_definitions('unit_defs.txt')

specific_price = []
for index, row in df.iterrows():
    unit = row['mass_unit']
    val = row['price']
    val = ureg.Quantity(val, unit)
    val = val.to('USD/kg').magnitude
    specific_price.append(val)
    # break

df['specific_price'] = specific_price


if not os.path.exists('output'): os.mkdir('output')

from es_utils.chem import process_chem_lookup

chem_lookup = pd.read_csv('chem_lookup.csv')
chem_lookup = process_chem_lookup(chem_lookup)
df = pd.merge(df, chem_lookup, on='original_name')


df.to_csv('output/processed.csv', index=False)


df = df.set_index('index')

df_combine = df.groupby('index')[['specific_price']].mean()

from es_utils import join_col_vals
df_combine['original_name']= df.groupby('index')['original_name'].apply(join_col_vals)
df_combine['molecular_formula']= df.groupby('index')['molecular_formula'].apply(join_col_vals)

from es_utils import extract_df_mat
df_price = extract_df_mat(df_combine)
df_price.to_csv('output/mat_data.csv')