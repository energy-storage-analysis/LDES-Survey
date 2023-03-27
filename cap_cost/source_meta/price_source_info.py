#%%
import pandas as pd
from es_utils.units import read_pint_df

import os
from os.path import join as pjoin

# %%


from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

dataset_folder = os.path.join(REPO_DIR,'cap_cost','datasets')
dataset_index = pd.read_csv(pjoin(dataset_folder,'dataset_index.csv'), index_col=0)

dfs_mat_data = []

for source, row in dataset_index.iterrows():
    fp_prices = os.path.join(dataset_folder, row['folder'], 'output', 'mat_data.csv')
    if os.path.exists(fp_prices):
        # df_mat_data = pd.read_csv(fp_prices, header = [0,1], index_col=0)
        df_mat_data = read_pint_df(fp_prices)
        
        df_mat_data['index_source'] = source

        if 'pub' in row['folder']:
            df_mat_data['type'] = 'Publication'
        else:
            df_mat_data['type'] = '-'

        dfs_mat_data.append(df_mat_data)


df_mat_data = pd.concat(dfs_mat_data)

#%%

df = df_mat_data[['index_source','source', 'type']]

df = df.rename({'source': 'sub_source'}, axis=1)

df['sub_source'] = df['sub_source'].fillna('None')

df_count = df.value_counts(['index_source', 'sub_source', 'type']).reset_index()

df_count = df_count.rename({0: 'count'}, axis=1)

df_count = df_count.sort_values(['index_source', 'count'])

df_count.to_csv('tables/price_source_counts.csv')


# %%

df_count

# #%%
# import pandas as pd

# #Manually specified types of sources
# df = pd.read_csv('tables/price_source_counts_edit.csv', index_col=0)

# df

# #%%

# import matplotlib.pyplot as plt

# fig, axes = plt.subplots(1,2, figsize=(10,5))

# df['type'].value_counts().plot.bar(ax= axes[0])
# axes[0].set_title('Source Counts')

# df.groupby('type')['count'].sum().plot.bar(ax=axes[1])

# axes[1].set_title('Price Entry Counts')

# plt.tight_layout()
# plt.savefig('figures/price_source_counts.png')


# #%%

# df_web = df[df['type'].isin(['Marketplace Website'])].dropna(how='all')
# df_web


# #%%


# df_web = df[df['type'].isin(['Commodity Analyst', 'Marketplace Website','Vendor Website'])].dropna(how='all').fillna("No Mention")

# fig, axes = plt.subplots(1,2, figsize=(10,5))

# df_web['notes'].value_counts().plot.bar(ax= axes[0])
# axes[0].set_title('Source Counts')

# df_web.groupby('notes')['count'].sum().plot.bar(ax=axes[1])
# axes[1].set_title('Price Entry Counts')

# #%%


# df_j = df[df['type'].isin(['Publication'])].dropna(how='all')

# fig, axes = plt.subplots(1,2, figsize=(10,8))

# df_j['notes'].value_counts().plot.bar(ax= axes[0])
# axes[0].set_title('Source Counts')

# df_j.groupby('notes')['count'].sum().sort_values(ascending=False).plot.bar(ax=axes[1])
# axes[1].set_title('Price Entry Counts')


# plt.tight_layout()
# plt.savefig('figures/publication_source_methods.png')

