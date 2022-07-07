"""Simple script to output a table dealing with a specific technology"""

#%%
import os
from os.path import join as pjoin
from es_utils.units import prep_df_pint_out, read_pint_df

output_dir = 'output/individual'
if not os.path.exists(output_dir): os.makedirs(output_dir)

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

df_SMs = read_pint_df(pjoin(REPO_DIR, 'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1])
df_SMs = df_SMs.reset_index('SM_type')

#%%

for SM_type in df_SMs['SM_type'].values:
    df_sel = df_SMs[df_SMs['SM_type'].isin([SM_type])].dropna(subset=['SM_type'])

    df_sel = df_sel.dropna(axis=1, how='all')

    df_sel = prep_df_pint_out(df_sel)

    df_sel.to_csv(os.path.join(output_dir,'{}.csv'.format(SM_type)))