#%%

import pandas as pd
from sympy import O
from es_utils.chem import get_molecular_mass
from es_utils.units import prep_df_pint_out

df = pd.read_csv('input.csv', index_col=0)
df['SM_type'] = 'synfuel'

df
# %%

deltaG_H2 = 0.0659 #kWh/molH2

total_deltaG = deltaG_H2*df['N_H2']

df['deltaG_chem'] = total_deltaG
df['n_e'] = 2*df['N_H2']



df
# %%

df_SM = df[['materials','mat_basis','SM_type','deltaG_chem','n_e']]


df_SM['deltaG_chem'] = df_SM['deltaG_chem'].astype('pint[kWh/mol]')
df_SM['n_e'] = df_SM['n_e'].astype('pint[dimensionless]')

df_SM = prep_df_pint_out(df_SM)

df_SM.to_csv('output/SM_data.csv')
# %%
