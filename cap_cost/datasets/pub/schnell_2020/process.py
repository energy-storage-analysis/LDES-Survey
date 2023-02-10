#%%

from os.path import join as pjoin
import os
import pandas as pd

from es_utils.units import convert_units, prep_df_pint_out, ureg

if not os.path.exists('output'): os.mkdir('output')


df = pd.read_excel('tables/table_s2.xlsx', sheet_name='Table S2 Material data')

df = df[['Unnamed: 2', 'Unnamed: 5', 'Unnamed: 6']]

df = df.dropna(how='all')
df = df.dropna(how='all', axis=1)

df.columns = ['original_name','specific_price','unit']


df = df.where(df['unit'] == '$/kg').dropna(how='all')

df = df.drop('unit', axis=1)

# df.to_csv('mat_lookup.csv')
df

#%%




mat_lookup = pd.read_csv('mat_lookup.csv', index_col=0)

from es_utils.chem import process_mat_lookup
mat_lookup = process_mat_lookup(mat_lookup)

df_mat = pd.merge(df, mat_lookup, on='original_name').set_index('index')

#%%

df_mat

#%%




from es_utils import extract_df_mat
from es_utils.units import read_pint_df
df_price = extract_df_mat(df_mat)

df_price = df_price.astype({
    'specific_price': 'pint[USD/kg]',
    })
# %%
df_price


df_price = convert_units(df_price)
df_price = prep_df_pint_out(df_price)


df_price.to_csv('output/mat_data.csv')

#%%