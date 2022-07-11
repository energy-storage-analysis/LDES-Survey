"""
Processing script template. This template is designed to work on extracted data (e.g. tables from pdf obtained from extract_template.py)
"""

#%%
import pandas as pd
import os
from es_utils.units import prep_df_pint_out, convert_units
from es_utils.chem import process_mat_lookup

if not os.path.exists('output'): os.mkdir('output')
tables = {fn.strip('.csv') : pd.read_csv(os.path.join('tables',fn), encoding='utf-8', index_col=0) for fn in os.listdir('tables')}
#%%

# Output the columns of a table into the Ipython console and copy to the rename dictonary below to rename the columns. 

df = tables['table_1']

df = df.rename({
'Theor. H2 capacity (wt.%) ': 'wt_pct', 
'DHdes/DHabs (kJ/mol.H2) ': 'H_des H_abs',
'DSdes/DSabs (J/mol.H2.K) ': 'dS_des dS_abs', 
'Hydride Crystal Density (g/cm3) ': 'mass_density',
'Theor. kg-H2/m3 wrt to hydride ': 'mass_density_H2', 
'Cost of H2 Storage (US$/kg-H2)a': 'H2_cost',
'1 bar H2 Desorption Temperature (-C)': 'T_desorb'
}, axis=1)

df.index.name = 'original_name'
# df = df.drop(['H_d'], axis=1)
df = df[['wt_pct']]

df['wt_pct'] = df['wt_pct']/100

df.index = df.index.str.replace('\n', '')
df.index = df.index.str.replace('þ',' ')

df


#%%

#TODO: add subtype

df_ch = df.iloc[1:8]
# df_ch['sub_type'] = 'complex_hydride' 
df_ch

df_im = df.iloc[9:]
# df_im['sub_type'] = 'intermetallic'
df_im

df2 = pd.concat([df_ch,df_im])

df2 = df2.dropna(subset=['wt_pct'])
df2


#%%


SM_lookup = pd.read_csv('SM_lookup.csv')

df_SM = pd.merge(df2, SM_lookup, on='original_name')
df_SM = df_SM.dropna(subset=['SM_name'])
df_SM = df_SM.set_index('SM_name')

from es_utils.chem import get_molecular_mass

df_SM['mu_host'] = df_SM['MF_host'].apply(get_molecular_mass)

mu_H = 1.0078


df_SM['r_H2'] = (df_SM['wt_pct']*df_SM['mu_host'])/((1-df_SM['wt_pct'])*mu_H )/2

deltaG_H2 = 0.0659 #kWh/molH2

df_SM['deltaG_chem'] = df_SM['r_H2'] * deltaG_H2
df_SM['n_e'] = df_SM['r_H2']*2

df_SM = df_SM[['SM_type','sub_type','mat_type','original_name','materials','mat_basis','deltaG_chem','n_e']]

df_SM['deltaG_chem'] = df_SM['deltaG_chem'].astype('pint[kWh/mol]')
df_SM['n_e'] = df_SM['n_e'].astype('pint[dimensionless]')

df_SM




#%%

# Map every column remaining (physical properties) that is not the specific price to the storage medium lookup and output



df_SM = convert_units(df_SM)
df_SM = prep_df_pint_out(df_SM)

df_SM.to_csv('output/SM_data.csv')
# %%
