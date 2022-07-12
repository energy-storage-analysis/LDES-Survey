"""Simple script to output a table dealing with a specific technology"""

#%%
import os
from os.path import join as pjoin

from matplotlib.pyplot import table
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

from pytablewriter import MarkdownTableWriter

tables_text = ""

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

    for col in df_sel.columns:
        if col[1] != 'N/U':
            df_sel[col] = df_sel[col].round(2)

    writer = MarkdownTableWriter(dataframe=df_sel.reset_index())


    tables_text = tables_text + "## {}".format(SM_type) + '\n\n'
    tables_text = tables_text + writer.dumps()
    tables_text = tables_text + "\n\n"


with open(os.path.join('output','SM_type_tables.md'.format(SM_type)), 'w', encoding='utf-8') as f:
    f.write(tables_text)

df_SM_source_info = pd.concat(dfs)


#%%
SM_source_info = df_SM_source_info['SM_sources'] + ': ' + df_SM_source_info['source_counts'].astype(str)

SM_source_info = SM_source_info.groupby(['SM_type','sub_type','mat_type']).apply(join_col_vals)

SM_source_info

#%%

SM_source_info.to_csv(pjoin('output','SM_source_info.csv'))

# %%

writer = MarkdownTableWriter(dataframe=SM_source_info.reset_index())


with open(os.path.join('output','source_info.md'), 'w', encoding='utf-8') as f:
    f.write(writer.dumps())

