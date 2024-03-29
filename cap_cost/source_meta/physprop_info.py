"""
Script to calculate teh total number of physical properties in the individual
datasets. The consolidated storage medium dataset combines physical properties
from multiple sources, so I don't think it's possible currently to figure out
the total number of physical properties obtained without iterating through the
raw datasets.
"""

#%%
import pandas as pd
from es_utils.units import read_pint_df

import os
from os.path import join as pjoin


from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')


physprop_lookup = pd.read_csv(os.path.join(REPO_DIR, 'cap_cost\data_consolidated\SM_column_info.csv'), index_col=0)

physprop_lookup
#%%


#%%

df_SMs = read_pint_df(pjoin(REPO_DIR,'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1]).reset_index('SM_type')

physprop_sources = df_SMs['SM_sources'].dropna().str.split(',')
physprop_sources


pp_num_sources = physprop_sources.apply(len).value_counts()
pp_num_sources

#%%

physprop_sources.apply(len).sum()

# (pp_num_sources*pp_num_sources.index).sum()
#%%


#%%

dataset_folder = os.path.join(REPO_DIR,'cap_cost','datasets')
dataset_index = pd.read_csv(pjoin(dataset_folder,'dataset_index.csv'), index_col=0)

dfs = []

for source, row in dataset_index.iterrows():
    fp_SM = os.path.join(dataset_folder, row['folder'], 'output', 'SM_data.csv')
    if os.path.exists(fp_SM):
        df_SM_data = read_pint_df(fp_SM)
        df_SM_data['source'] = source

        present_physprop = [p for p in physprop_lookup.index if p in df_SM_data.columns]
        df_pp = df_SM_data[['source', *present_physprop]]

        dfs.append(df_pp)

        # break



df_all = pd.concat(dfs)



import numpy as np

# We remove these deltaG_chem as they are duplicate values. 
df_all['deltaG_chem'][['H2 Spherical Pressure', 'CH4 Spherical Pressure', 'LNG Tank', 'LH2 Tank', 'CH4 (Salt)', 'H2 (Salt)', 'CH4 (LRC)', 'H2 (LRC)', 'Fossil CH4']] = np.nan
df_all['n_e'][['H2 Spherical Pressure', 'CH4 Spherical Pressure', 'LNG Tank', 'LH2 Tank', 'CH4 (Salt)', 'H2 (Salt)', 'CH4 (LRC)', 'H2 (LRC)', 'Fossil CH4']] = np.nan
# df_all[['source', 'deltaG_chem']].dropna()


df_all = df_all.drop('kth', axis = 1) #Unused
df_all = df_all.drop('vol_latent_heat', axis = 1) #Unused

#%%
df_all[['source', 'delta_height']].dropna()


# %%

physprop_counts = df_all.drop('source', axis=1).count()

#We manually fix the counts for the three viral theorem technologies which have dulplicates.
physprop_counts['specific_strength'] = physprop_counts['specific_strength']/3
physprop_counts['Qmax'] = 3

physprop_counts.to_csv('tables/physprop_counts.csv')

#%%


print("Total physical properties collected that are used in calculations: {}".format(physprop_counts.sum()))


#%%

#TODO: Some of the above analysis might not be required with the addition of SM_all

df_SM = read_pint_df(pjoin(REPO_DIR,'cap_cost/data_consolidated/SM_data_all.csv'), index_col=[0,1])
df_SM
# %%


physprop_lookup

#%%

def num_unique(l):
    return len(l.unique())

df_duplicated = []

for col in physprop_lookup.index:

    if col == 'T_min' or col=='deltaT':
        continue #TODO: This is calculated after consolidation....

    s_sel = df_SM[col].dropna()
    s_grouped = s_sel.groupby(by=['SM_name','SM_type']).apply(num_unique)

    s_grouped = s_grouped.where(s_grouped > 1).dropna()

    df_stat = df_SM[col].loc[s_grouped.index].groupby(by=['SM_name','SM_type']).agg(
        ['count','min','max','mean','std']
    )

    df_stat['property'] = col
    df_stat = df_stat[['property','count','min','max','mean','std']]


    df_duplicated.append(df_stat)




from es_utils.units import prep_df_pint_out

df_duplicated = pd.concat(df_duplicated)

# df_duplicated = prep_df_pint_out(df_duplicated)



df_duplicated.to_csv('tables/physprop_duplicated.csv')
