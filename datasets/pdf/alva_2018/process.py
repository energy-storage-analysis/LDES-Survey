#%%

import pandas as pd

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import seaborn as sns
sys.path.append('..')

# Alva Thermal
df_latent = pd.read_csv('tables/table_8.csv', index_col=0)

df_latent['C_kwh'] = df_latent['cost']/(df_latent['sp_latent_heat'])
df_latent['energy_type'] = 'Latent Thermal'# (T > 200 C)'
df_latent['source'] = 'Alva et al. 2018'
df_latent = df_latent.where(df_latent['phase_change_T'] > 200).dropna(subset=['phase_change_T'])

df_latent = df_latent.rename({'material':'name'}, axis=1)

#%%

df_latent['name'] = df_latent['name'].replace('Zn/Mg (53.7/46.3)', 'Zn54Mg46')
df_latent['name'] = df_latent['name'].replace('Zn/Al (96/4)', 'Zn96Al4')
df_latent['name'] = df_latent['name'].replace('Al/Mg/Zn (59/33/6)', 'Al59Mg33Zn6')
df_latent['name'] = df_latent['name'].replace('Al/Mg/Zn (60/34/6)', 'Al60Mg34Zn6')
df_latent['name'] = df_latent['name'].replace('Mg/Cu/Zn (60/25/15)', 'Mg60Cu25Zn15')
df_latent['name'] = df_latent['name'].replace('Mg/Ca (84/16)', 'Mg84Ca16')
df_latent['name'] = df_latent['name'].replace('Mg/Si/Zn (47/38/15)', 'Mg47Si38Zn15')
df_latent['name'] = df_latent['name'].replace('Cu/Si (80/20)', 'Cu80Si20')
df_latent['name'] = df_latent['name'].replace('Cu/P/Si (83/10/7)', 'Cu83P10Si7')
df_latent['name'] = df_latent['name'].replace('Si/Mg/Ca (49/30/21)', 'Si49Mg30Ca21')
df_latent['name'] = df_latent['name'].replace('Si/Mg (56/44)', 'Si56Mg44')

df_latent['name'] = df_latent['name'].replace('Copper', 'Cu')
df_latent['name'] = df_latent['name'].replace('Zinc', 'Zn')
df_latent['name'] = df_latent['name'].replace('Aluminum', 'Al')

df_latent

#%%
df_latent.to_csv('output/latent.csv')

#%%
df_4 = pd.read_csv('tables/table_4.csv', index_col=0)
df_5 = pd.read_csv('tables/table_5.csv', index_col=0)
df_6 = pd.read_csv('tables/table_6.csv', index_col=0)
df_7 = pd.read_csv('tables/table_7.csv', index_col=0)

col_sel = ['Cp', 'kth', 'cost', 'class']

df_sens = pd.concat([df[col_sel] for df in [df_4, df_5, df_6, df_7]])
df_sens = df_sens.reset_index() #name was the index
df_sens['Cp'] = df_sens['Cp']/3600
df_sens['C_kwh'] = df_sens['cost']/(df_sens['Cp']*500)

df_sens['energy_type'] = 'Sensible Thermal'
df_sens['source'] = 'Alva et al. 2018'
df_sens
# %%
df_sens.to_csv('output/sensible.csv')