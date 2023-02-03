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

#%%


dfs = []

for SM_type in set(df_SMs['SM_type'].values):
    df_sel = df_SMs[df_SMs['SM_type'] == SM_type].dropna(subset=['SM_type'])

    df_sel = df_sel.dropna(subset=['C_kwh'])
    df_sel = df_sel.dropna(axis=1, how='all')

    if 'sub_type' not in df_sel.columns:
        df_sel['sub_type'] = ''

    if 'mat_type' not in df_sel.columns:
        df_sel['mat_type'] = ''

    df_sel['sub_type'] = df_sel['sub_type'].fillna('None')
    df_sel['mat_type'] = df_sel['mat_type'].fillna('None')

    df_SM_source_info = df_sel.groupby(['sub_type', 'mat_type'])['SM_sources'].value_counts()
    df_SM_source_info.name = 'source_counts'

    df_SM_source_info = df_SM_source_info.reset_index()
    df_SM_source_info['SM_type'] = SM_type
    df_SM_source_info  = df_SM_source_info.set_index(['SM_type','sub_type','mat_type'])
    dfs.append(df_SM_source_info)

    # output individual files

    df_sel = df_sel.drop('SM_type', axis=1)

    if SM_type != 'sensible_thermal' and 'T_min' in df_sel.columns:
        df_sel = df_sel.drop('T_min', axis=1)

    df_sel = prep_df_pint_out(df_sel)

    df_sel.to_csv(os.path.join(output_dir,'{}.csv'.format(SM_type)))


df_SM_source_info = pd.concat(dfs)


#%%
SM_source_info = df_SM_source_info['SM_sources'] + ': ' + df_SM_source_info['source_counts'].astype(str)

SM_source_info = SM_source_info.groupby(['SM_type','sub_type','mat_type']).apply(join_col_vals)

SM_source_info.name = 'SM Sources'

#%%

SM_source_info.to_csv(pjoin('tables','SM_type_source_counts.csv'))

# %%

from es_utils import join_col_vals

df_type_lists = SM_source_info.reset_index().drop('SM Sources', axis=1)
sub_types = df_type_lists.groupby('SM_type')['sub_type'].apply(join_col_vals)
mat_types = df_type_lists.groupby('SM_type')['mat_type'].apply(join_col_vals)

# %%

df_type_lists = pd.concat([sub_types,mat_types], axis=1)

df_type_lists.to_csv(pjoin('tables','SM_type_sub_mat_lists.csv'))