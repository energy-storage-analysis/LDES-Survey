"""
This script generates tables with information/stats about the final dataset
"""
#%%
from es_utils.units import read_pint_df, ureg

import os
from os.path import join as pjoin
output_dir = 'output'
if not os.path.exists(output_dir): os.makedirs(output_dir)

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

df_SMs = read_pint_df(pjoin(REPO_DIR,'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True).reset_index('SM_type')
df_mat_data = read_pint_df(pjoin(REPO_DIR, 'cap_cost/data_consolidated/mat_data.csv'), index_col=0, drop_units=True)

# %%

#TODO: shouldn't this happen on load?
df_SMs['C_kwh'] = df_SMs['C_kwh'].astype('pint[USD/kWh]')

cutoff = ureg.Quantity(10, 'USD/kWh')

below_cufoff = [c < cutoff for c in df_SMs['C_kwh'].values]
df_sel = df_SMs[below_cufoff].dropna(how='all')

df_sel = df_sel[['SM_type','specific_energy','specific_price','price_sources','SM_sources','C_kwh']]

df_sel = df_sel.round(3)
df_sel = df_sel.sort_values('C_kwh')

# df_sel = df_sel.reset_index('SM_type')
df_sel['SM_type'] = df_sel['SM_type'].str.replace('_', ' ')
df_sel['SM_type'] = df_sel['SM_type'].str.replace('thermochemical', 'thermo-chemical')


#TODO: come up with some sort of long name (and units) system for displayed tables
df_sel.columns = [c.replace('_',' ') for c in df_sel.columns]


df_sel.to_csv('output/SM_downselected.csv')

# %%
