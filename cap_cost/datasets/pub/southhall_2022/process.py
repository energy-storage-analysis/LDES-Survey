#%%

import pandas as pd
from sympy import O
from es_utils.chem import get_molecular_mass
from es_utils.units import prep_df_pint_out

df_SM = pd.read_csv('input.csv', index_col=0)
df_SM['SM_type'] = 'synfuel'
df_SM['sub_type'] = 'chemical'
df_SM['mat_type'] = 'LOHC'

df_SM['wt_pct'] = df_SM['wt_pct']/100

df_SM['mu_host'] = df_SM['MF_host'].apply(get_molecular_mass)

mu_H = 1.0078


df_SM['r_H2'] = (df_SM['wt_pct']*df_SM['mu_host'])/((1-df_SM['wt_pct'])*mu_H )/2

deltaG_H2 = 0.0659 #kWh/molH2

df_SM['deltaG_chem'] = df_SM['r_H2'] * deltaG_H2
df_SM['n_e'] = df_SM['r_H2']*2

# df_SM = df_SM[['original_name','SM_type','sub_type','materials','mat_basis','deltaG_chem','n_e']]

df_SM['deltaG_chem'] = df_SM['deltaG_chem'].astype('pint[kWh/mol]')
df_SM['n_e'] = df_SM['n_e'].astype('pint[dimensionless]')

df_SM



# deltaG_H2 = 0.0659 #kWh/molH2

# total_deltaG = deltaG_H2*df['N_H2']

# df['deltaG_chem'] = total_deltaG
# df['n_e'] = 2*df['N_H2']



df_SM
# %%

df_SM = df_SM[['SM_type','sub_type','mat_type','materials','mat_basis','deltaG_chem','n_e']]


df_SM['deltaG_chem'] = df_SM['deltaG_chem'].astype('pint[kWh/mol]')
df_SM['n_e'] = df_SM['n_e'].astype('pint[dimensionless]')

df_SM = prep_df_pint_out(df_SM)

df_SM.to_csv('output/SM_data.csv')
# %%
