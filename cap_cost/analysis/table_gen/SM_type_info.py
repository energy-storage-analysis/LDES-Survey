"""Simple script to output a table dealing with a specific technology"""

#%%
import os
from os.path import join as pjoin
from es_utils.units import prep_df_pint_out, read_pint_df
from es_utils import join_col_vals
import pandas as pd

output_dir = 'output/individual'
if not os.path.exists(output_dir): os.makedirs(output_dir)

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

df_SMs = read_pint_df(pjoin(REPO_DIR, 'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1])
df_SMs = df_SMs.reset_index('SM_type')

#%%

dfs = []

for SM_type in set(df_SMs['SM_type'].values):
    df_sel = df_SMs[df_SMs['SM_type'] == SM_type].dropna(subset=['SM_type'])

    df_sel = df_sel.dropna(axis=1, how='all')

    if 'sub_type' not in df_sel.columns:
        df_sel['sub_type'] = ''

    df_sel['sub_type'] = df_sel['sub_type'].fillna('None')

    df_SM_source_info = df_sel.groupby('sub_type')['SM_sources'].value_counts()
    df_SM_source_info.name = 'source_counts'

    df_SM_source_info = df_SM_source_info.reset_index()
    df_SM_source_info['SM_type'] = SM_type
    df_SM_source_info  = df_SM_source_info.set_index(['SM_type','sub_type'])
    dfs.append(df_SM_source_info)

    df_sel = prep_df_pint_out(df_sel)

    df_sel.to_csv(os.path.join(output_dir,'{}.csv'.format(SM_type)))


df_SM_source_info = pd.concat(dfs)


#%%
SM_source_info = df_SM_source_info['SM_sources'] + ': ' + df_SM_source_info['source_counts'].astype(str)

SM_source_info = SM_source_info.groupby(['SM_type','sub_type']).apply(join_col_vals)

SM_source_info

#%%

SM_source_info.to_csv(pjoin('output','SM_source_info.csv'))

# %%
