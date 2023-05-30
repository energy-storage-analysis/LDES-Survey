
"""
Outputs markdown tables of information related to specific technology classes
SM_type_tables.md: detailed entries for each type 
source_info.md: tech type counts for each source
"""

#%%
import os
from os.path import join as pjoin

from matplotlib.pyplot import table
from es_utils.units import prep_df_pint_out, read_pint_df
from es_utils import join_col_vals
import pandas as pd

output_dir = 'tables/individual'
if not os.path.exists(output_dir): os.makedirs(output_dir)

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

df_SMs = read_pint_df(pjoin(REPO_DIR, 'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1])
df_SMs = df_SMs.reset_index('SM_type')

# %%

multiple_sources = df_SMs['SM_sources'].dropna().str.split(',').apply(len).sort_values(ascending=False)
multiple_sources = multiple_sources.where(multiple_sources>1).dropna()

multiple_sources


# %%

df_SMs.loc[multiple_sources.index].to_csv('tables/multiple_sources.csv')