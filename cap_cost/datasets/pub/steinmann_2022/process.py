#%%
import pandas as pd
import numpy as np
import os

if not os.path.exists('output'): os.mkdir('output')
tables = {fn.strip('.csv') : pd.read_csv(os.path.join('tables',fn), encoding='utf-8', index_col=0) for fn in os.listdir('tables')}
#%%

df = tables['table_21']

df = df.rename({
'Temperature range [°C]': "T_range", 
'Spec Heat capacity [J/kgK]': 'Cp',
'Density [kg/m3] ': 'mass_density', 
'Estimated Material cost [€/ton]': 'specific_price'
}, axis=1)


df.index.name = 'original_name'

from es_utils.pdf import average_range

df['Cp'] = df['Cp']/3600000
df['specific_price'] = df['specific_price'].fillna('').apply(average_range).replace('',np.nan).astype(float)
df['specific_price'] = df['specific_price']/1000

df['T_range'] = df['T_range'].str.replace('\n','').str.replace('°C','')

df[['T_low', 'T_high']] = df['T_range'].str.split('-', expand=True)[[0,1]]

# df['deltaT']

df = df.drop('T_range', axis=1)


df

df = pd.concat([
df.iloc[1:4],#.assign(Type='Molten Salt'),
df.iloc[7:8],#.assign(Type='Liquid Metals'),
df.iloc[10:11],#.assign(Type='Mineral Oil'),
df.iloc[12:13],#.assign(Type='Synthetic Liquid'),
df.iloc[14:15],#.assign(Type='Element'),
df.iloc[16:17]#.assign(Type='Vegetable oil'),
])


df

# df.to_csv('SM_lookup_temp.csv')
#%%

# df = df.rename({}, axis=1)

df_SM = df[['Cp', 'mass_density','T_low', 'T_high']]

SM_lookup = pd.read_csv('SM_lookup.csv')
df_SM = pd.merge(df_SM, SM_lookup, on='original_name')
df_SM = df_SM.dropna(subset=['SM_name'])
df_SM = df_SM.set_index('SM_name')

df_SM.to_csv('output/SM_data.csv')

df_mat = df[['specific_price']]

chem_lookup = pd.read_csv('chem_lookup.csv')
df_mat = pd.merge(df_mat, chem_lookup, on='original_name')
df_mat = df_mat.dropna(subset=['index'])
df_mat = df_mat.set_index('index')

df_mat.to_csv('output/mat_data.csv')

# %%
