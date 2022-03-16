#%%

from operator import index
import pandas as pd

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import seaborn as sns
import es_utils

chem_lookup = pd.read_csv('chem_lookup.csv')
chem_lookup = es_utils.chem.process_chem_lookup(chem_lookup)

# Alva Thermal
df_latent = pd.read_csv('tables/table_8.csv', index_col=0)

df_latent['specific_energy'] = df_latent['sp_latent_heat']/3600 #TODO: units
df_latent = df_latent.drop('sp_latent_heat',axis=1)


#Only keep data relevant to high temperature storage (not buildings)
df_latent = df_latent.where(df_latent['phase_change_T'] > 200).dropna(subset=['phase_change_T']).reset_index(drop=True)

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

#If no lookup table is needed
from es_utils.chem import mat2vec_process

from mat2vec.processing import MaterialsTextProcessor
mtp = MaterialsTextProcessor()

df_latent['molecular_formula'] = df_latent['original_name'].apply(lambda x: mat2vec_process(x, mtp))

index_use = 'molecular_formula'
df_latent['index_use'] = index_use
df_latent['index'] = df_latent[index_use]
df_latent = df_latent.set_index('index')
#%%

df_latent['energy_type'] = 'latent_thermal'


#%%
df_latent.to_csv('output/latent.csv')

#%%
df_4 = pd.read_csv('tables/table_4.csv')
df_5 = pd.read_csv('tables/table_5.csv')



df_6 = pd.read_csv('tables/table_6.csv')
df_7 = pd.read_csv('tables/table_7.csv')

col_sel = ['original_name','Cp', 'kth', 'specific_price', 'class']

df_sens = pd.concat([df[col_sel] for df in [df_4, df_5, df_6, df_7]]).dropna(subset=['original_name'])

#%%


df_sens = pd.merge(df_sens, chem_lookup, on='original_name').set_index('index')
#%%
#TODO: Units
df_sens['Cp'] = df_sens['Cp']/3600

#TODO: How to have consistent naming without introducing delta T?
df_sens['specific_energy'] = df_sens['Cp']*500
# df_sens['C_kwh'] = df_sens['specific_price']/(df_sens['Cp']*500)
df_sens['energy_type'] = 'sensible_thermal'
# %%
df_sens.to_csv('output/sensible.csv')
# %%

# %%
