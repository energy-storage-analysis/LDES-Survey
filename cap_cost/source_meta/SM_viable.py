"""
This script generates tables with information/stats about the final dataset
"""
#%%
from es_utils.units import read_pint_df, ureg

import os
from os.path import join as pjoin
output_dir = 'tables'
if not os.path.exists(output_dir): os.makedirs(output_dir)

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

df_SMs = read_pint_df(pjoin(REPO_DIR,'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1]).reset_index('SM_type')

# %%

#TODO: shouldn't this happen on load?
df_SMs['C_kwh'] = df_SMs['C_kwh'].astype('pint[USD/kWh]')

cutoff = ureg.Quantity(10, 'USD/kWh')

below_cufoff = [c < cutoff for c in df_SMs['C_kwh'].values]
df_sel = df_SMs[below_cufoff].dropna(how='all')

df_sel = df_sel[['SM_type','specific_energy','specific_price','price_sources','SM_sources','C_kwh']]

# df_sel = df_sel.round(3)
df_sel = df_sel.sort_values('C_kwh')

# df_sel = df_sel.reset_index('SM_type')


from es_utils.units import prep_df_pint_out

df_sel = prep_df_pint_out(df_sel)

df_sel.to_csv('tables/SM_viable.csv')

# %%
