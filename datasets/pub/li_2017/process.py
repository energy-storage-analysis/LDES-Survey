#%%
import numpy as np
import pandas as pd
import os
from es_utils import chem

from es_utils.chem import process_chem_lookup
from mat2vec.processing import MaterialsTextProcessor
mtp = MaterialsTextProcessor()

chem_lookup = pd.read_csv('chem_lookup.csv')
chem_lookup = process_chem_lookup(chem_lookup, mtp=None)
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
SM_lookup




from es_utils.chem import mat2vec_process

def normalize_list(l_str):
    l = l_str.strip('][').split(', ')
    list_out = []
    for f in l:
        list_out.append(mat2vec_process(f, mtp))
    list_out = str(list_out)
    return list_out

# SM_lookup['materials'] = SM_lookup['materials'].apply(normalize_list)

#%%

df_SM = pd.merge(df, SM_lookup, on='original_name')

df_SM['energy_type'] = 'electrochemical'
df_SM.index.name = 'SM_name'

df_SM = df_SM[['C_kwh_orig','type','deltaV','materials','energy_type']]

df_SM.to_csv('output/SM_data.csv')


