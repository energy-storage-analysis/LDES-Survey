"""
This script generates tables with information/stats about the final dataset
"""
#%%
import pandas as pd
from es_utils.units import read_pint_df

import os
from os.path import join as pjoin

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

df_SMs = read_pint_df(pjoin(REPO_DIR,'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True).reset_index('SM_type')
df_mat_data = read_pint_df(pjoin(REPO_DIR, 'cap_cost/data_consolidated/mat_data.csv'), index_col=0, drop_units=True)

#%%

df_mat_unused = df_mat_data[df_mat_data['num_SMs'] == 0].dropna(how='all')
df_mat_unused.to_csv('tables/mat_data_unused.csv')

df_mat_data = df_mat_data[df_mat_data['num_SMs'] > 0].dropna(how='all')
df_mat_data.to_csv('tables/mat_data_used.csv')

from collections import Counter

def get_source_SM_counts(df):
    counts = Counter(df)
    counts = str(dict(counts))
    return counts

SM_source_info = df_SMs.groupby('SM_sources')['SM_type'].apply(get_source_SM_counts).dropna()
SM_source_info.name = 'SM types'

price_source_info = df_mat_data.groupby('sources').apply(len)
price_source_info.name = 'num prices'

source_info = pd.concat([SM_source_info, price_source_info],axis=1 )

source_info = source_info.sort_index()

source_info['num prices'] = source_info['num prices'].fillna(0).astype(int).astype(str).str.replace('^0$','-',regex=True)
source_info['SM types'] = source_info['SM types'].fillna('-')

source_info.to_csv('tables/source_combo_counts.csv')
