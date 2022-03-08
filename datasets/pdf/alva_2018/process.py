#%%

import pandas as pd

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import seaborn as sns
sys.path.append('..')

# Alva Thermal
df_latent = pd.read_csv('tables/table_8.csv')

df_latent['C_kwh'] = df_latent['cost']/(df_latent['sp_latent_heat'])

#Only keep data relevant to high temperature storage (not buildings)
df_latent = df_latent.where(df_latent['phase_change_T'] > 200).dropna(subset=['phase_change_T'])

#%%

df_latent['original_name'] = df_latent['original_name'].replace('Zn/Mg (53.7/46.3)', 'Zn54Mg46')
df_latent['original_name'] = df_latent['original_name'].replace('Zn/Mg (52/48)', 'Zn52Mg48')
df_latent['original_name'] = df_latent['original_name'].replace('Zn/Al (96/4)', 'Zn96Al4')
df_latent['original_name'] = df_latent['original_name'].replace('Al/Mg/Zn (59/33/6)', 'Al59Mg33Zn6')
df_latent['original_name'] = df_latent['original_name'].replace('Al/Mg/Zn (60/34/6)', 'Al60Mg34Zn6')
df_latent['original_name'] = df_latent['original_name'].replace('Mg/Cu/Zn (60/25/15)', 'Mg60Cu25Zn15')
df_latent['original_name'] = df_latent['original_name'].replace('Mg/Ca (84/16)', 'Mg84Ca16')
df_latent['original_name'] = df_latent['original_name'].replace('Mg/Si/Zn (47/38/15)', 'Mg47Si38Zn15')
df_latent['original_name'] = df_latent['original_name'].replace('Cu/Si (80/20)', 'Cu80Si20')
df_latent['original_name'] = df_latent['original_name'].replace('Cu/P/Si (83/10/7)', 'Cu83P10Si7')
df_latent['original_name'] = df_latent['original_name'].replace('Si/Mg/Ca (49/30/21)', 'Si49Mg30Ca21')
df_latent['original_name'] = df_latent['original_name'].replace('Si/Mg (56/44)', 'Si56Mg44')

df_latent['original_name'] = df_latent['original_name'].replace('Copper', 'Cu')
df_latent['original_name'] = df_latent['original_name'].replace('Zinc', 'Zn')
df_latent['original_name'] = df_latent['original_name'].replace('Aluminum', 'Al')

df_latent = df_latent.rename({'original_name': 'molecular_formula'}, axis=1)

#%%
df_latent.to_csv('output/latent.csv')

#%%
df_4 = pd.read_csv('tables/table_4.csv')
df_5 = pd.read_csv('tables/table_5.csv')



df_6 = pd.read_csv('tables/table_6.csv')
df_7 = pd.read_csv('tables/table_7.csv')

col_sel = ['original_name','Cp', 'kth', 'cost', 'class']

df_sens = pd.concat([df[col_sel] for df in [df_4, df_5, df_6, df_7]]).dropna(subset=['original_name'])


chem_lookup = pd.read_csv('chem_lookup.csv', index_col=0)

present_chemicals = df_sens['original_name'].values

df_sens['material_name'] = chem_lookup.loc[present_chemicals]['material_name'].values
df_sens['molecular_formula'] = chem_lookup.loc[present_chemicals]['molecular_formula'].values

df_sens['Cp'] = df_sens['Cp']/3600
df_sens['C_kwh'] = df_sens['cost']/(df_sens['Cp']*500)
df_sens
# %%
df_sens.to_csv('output/sensible.csv')