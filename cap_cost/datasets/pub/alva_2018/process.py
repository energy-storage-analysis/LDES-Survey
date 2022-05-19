#%%

import numpy as np
import pandas as pd
import pint_pandas
import es_utils
import pint

from es_utils.units import ureg

chem_lookup = pd.read_csv('chem_lookup.csv')
chem_lookup = es_utils.chem.process_chem_lookup(chem_lookup)

# Alva Thermal
df_latent = pd.read_csv('tables/table_8.csv')

df_latent = df_latent.set_index('original_name')

df_latent = df_latent.rename({'density': 'mass_density'}, axis=1)
df_latent['mass_density'] = df_latent['mass_density'].str.replace("\d+\ ?\(L.*\)", 'nan') 
df_latent['mass_density'] = df_latent['mass_density'].str.replace("(\d+) ?\(S.*\).?", r'\1')
df_latent['mass_density'] = df_latent['mass_density'].astype(float) #kg/m3

df_latent['kth'] = df_latent['kth'].str.replace('\(S.*\)','')
df_latent['kth'] = df_latent['kth'].str.replace('\S+ ?\(L.*\)','nan').astype(float)

#%%

df_latent = df_latent.astype({
    'sp_latent_heat': 'pint[kJ/kg]', 
    'phase_change_T': 'pint[degC]',
    'kth': 'pint[W/m/K]',
    'vol_latent_heat': 'pint[MJ/m**3]',
    'specific_price': 'pint[USD/kg]',
    'mass_density': 'pint[kg/m**3]'
    })

from es_utils.units import prep_df_pint_out, convert_units



df_latent = convert_units(df_latent)

# #Only keep data relevant to high temperature storage (not buildings)
high_T = [T > ureg.Quantity(200, 'degC') for T in df_latent['phase_change_T']] 
df_latent = df_latent[high_T].dropna(subset=['phase_change_T'])

#%%
from pint import Quantity
df_4 = pd.read_csv('tables/table_4.csv')
df_5 = pd.read_csv('tables/table_5.csv')
df_6 = pd.read_csv('tables/table_6.csv')
df_7 = pd.read_csv('tables/table_7.csv')

df_sens = pd.concat([df_4, df_5, df_6, df_7]).dropna(subset=['original_name'])
df_sens = df_sens.set_index('original_name')


df_sens['T_melt'] = df_sens['T_melt'].replace('e','nan')
df_sens['T_max'] = df_sens['T_max'].replace('e','nan').astype(float)

df_sens = df_sens.astype({
    'Cp': 'pint[kJ/kg/degC]',
    'T_melt': 'pint[degC]',
    'T_max': 'pint[degC]',
    'kth':'pint[W/m/K]',
    'specific_price': 'pint[USD/kg]'
    })


df_sens = convert_units(df_sens)

#%%

df = pd.concat([
    df_latent,
    df_sens
])

df_mat = pd.merge(df, chem_lookup, on='original_name').set_index('index')




df_mat = es_utils.extract_df_mat(df_mat)

df_mat = prep_df_pint_out(df_mat)
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

df_SMs = df_SMs[['materials','mat_basis','original_name','SM_type','Cp', 'T_melt','T_max', 'phase_change_T','sp_latent_heat','mass_density','kth','vol_latent_heat']]


df_SMs = prep_df_pint_out(df_SMs)


df_SMs.to_csv('output/SM_data.csv')
# %%
