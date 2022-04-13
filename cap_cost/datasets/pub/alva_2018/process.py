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
df_latent = pd.read_csv('tables/table_8.csv')

df_latent['sp_latent_heat'] = df_latent['sp_latent_heat']/3600 #TODO: units
# df_latent = df_latent.drop('sp_latent_heat',axis=1)


#Only keep data relevant to high temperature storage (not buildings)
df_latent = df_latent.where(df_latent['phase_change_T'] > 200).dropna(subset=['phase_change_T']).reset_index(drop=True)

#%%

# df_latent['original_name'] = df_latent['original_name'].replace('Zn/Mg (53.7/46.3)', 'Zn54Mg46')
# df_latent['original_name'] = df_latent['original_name'].replace('Zn/Mg (52/48)', 'Zn52Mg48')
# df_latent['original_name'] = df_latent['original_name'].replace('Zn/Al (96/4)', 'Zn96Al4')
# df_latent['original_name'] = df_latent['original_name'].replace('Al/Mg/Zn (59/33/6)', 'Al59Mg33Zn6')
# df_latent['original_name'] = df_latent['original_name'].replace('Al/Mg/Zn (60/34/6)', 'Al60Mg34Zn6')
# df_latent['original_name'] = df_latent['original_name'].replace('Mg/Cu/Zn (60/25/15)', 'Mg60Cu25Zn15')
# df_latent['original_name'] = df_latent['original_name'].replace('Mg/Ca (84/16)', 'Mg84Ca16')
# df_latent['original_name'] = df_latent['original_name'].replace('Mg/Si/Zn (47/38/15)', 'Mg47Si38Zn15')
# df_latent['original_name'] = df_latent['original_name'].replace('Cu/Si (80/20)', 'Cu80Si20')
# df_latent['original_name'] = df_latent['original_name'].replace('Cu/P/Si (83/10/7)', 'Cu83P10Si7')
# df_latent['original_name'] = df_latent['original_name'].replace('Si/Mg/Ca (49/30/21)', 'Si49Mg30Ca21')
# df_latent['original_name'] = df_latent['original_name'].replace('Si/Mg (56/44)', 'Si56Mg44')

# df_latent['original_name'] = df_latent['original_name'].replace('Copper', 'Cu')
# df_latent['original_name'] = df_latent['original_name'].replace('Zinc', 'Zn')
# df_latent['original_name'] = df_latent['original_name'].replace('Aluminum', 'Al')


df_latent = df_latent.set_index('original_name')

#If no lookup table is needed
from es_utils.chem import pymatgen_process




#%%



#%%

#%%
df_4 = pd.read_csv('tables/table_4.csv')
df_5 = pd.read_csv('tables/table_5.csv')
df_6 = pd.read_csv('tables/table_6.csv')
df_7 = pd.read_csv('tables/table_7.csv')


df_sens = pd.concat([df_4, df_5, df_6, df_7]).dropna(subset=['original_name'])

df_sens = df_sens.set_index('original_name')

#%%


# df_sens = pd.merge(df_sens, chem_lookup, on='original_name').set_index('index')
#%%
#TODO: Units
df_sens['Cp'] = df_sens['Cp']/3600

#TODO: How to have consistent naming without introducing delta T?
# df_sens['specific_energy'] = df_sens['Cp']*500
# df_sens['C_kwh'] = df_sens['specific_price']/(df_sens['Cp']*500)

#%%

df = pd.concat([
    df_latent,
    df_sens
])

df_mat = pd.merge(df, chem_lookup, on='original_name').set_index('index')

df_mat = es_utils.extract_df_mat(df_mat)
df_mat
#%%

df_mat.to_csv('output/mat_data.csv')


# %%


SM_lookup = pd.read_csv('SM_lookup.csv', index_col=0)

df_SMs = pd.merge(
    SM_lookup,
    df,
    on='original_name'
    
)

#%%

# df_SMs.index.name = 'SM_name'
df_SMs = df_SMs.reset_index().set_index('SM_name')

df_SMs = df_SMs[['materials','original_name','SM_type','Cp', 'T_melt','T_max', 'phase_change_T','sp_latent_heat','density','kth','vol_latent_heat']]

df_SMs['T_melt'] = df_SMs['T_melt'].replace('e','')
df_SMs['T_max'] = df_SMs['T_max'].replace('e','')

df_SMs = df_SMs.rename({'density': 'mass_density'}, axis=1)
df_SMs['mass_density'] = df_SMs['mass_density'].str.strip('(S)').astype(float) #kg/m3

df_SMs.to_csv('output/SM_data.csv')
# %%
