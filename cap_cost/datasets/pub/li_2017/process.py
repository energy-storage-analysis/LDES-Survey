#%%
import numpy as np
import pandas as pd
import os
from es_utils import chem

from es_utils.chem import process_chem_lookup


chem_lookup = pd.read_csv('chem_lookup.csv')
chem_lookup = process_chem_lookup(chem_lookup)
# %%
table_3 = pd.read_csv('tables/table_3.csv', index_col=0)
table_3

#%%


added_rows = pd.DataFrame({
    'molecular_formula': ['O2'],
    'ref': [np.nan],
    'specific_price': [0]
}, index = ['Air'])
added_rows.index.name ='index'

table_3 = pd.merge(table_3, chem_lookup, on='original_name').set_index('index')

table_3 = table_3.append(added_rows)

# %%

from es_utils import extract_df_mat
df_price = extract_df_mat(table_3)
df_price.to_csv('output/mat_data.csv')

#%%
df = pd.read_csv('tables/table_2.csv')

df = df.rename({'C_kwh': 'C_kwh_orig'}, axis=1)

df = df.dropna(how='all')

df = df.drop('ref',axis=1)

df = df.rename({'label':'original_name'}, axis=1).set_index('original_name')

df

# %%

SM_lookup = pd.read_csv('SM_lookup.csv', index_col=0)

df_SM = pd.merge(df, SM_lookup, on='original_name')

df_SM.index.name = 'SM_name'

df_SM = df_SM[['C_kwh_orig','type','deltaV','materials','mat_basis','SM_type']]

df_SM.to_csv('output/SM_data.csv')


