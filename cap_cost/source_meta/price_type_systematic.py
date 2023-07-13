#%%

# make lookup 

#%%
import pandas as pd
from es_utils.units import read_pint_df

import matplotlib.pyplot as plt

import os
from os.path import join as pjoin

# %%


from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

dataset_folder = os.path.join(REPO_DIR,'cap_cost','datasets')
dataset_index = pd.read_csv(pjoin(dataset_folder,'dataset_index.csv'), index_col=0)

dfs_mat_data = []

price_sources = []
price_folders = []

for source, row in dataset_index.iterrows():
    fp_prices = os.path.join(dataset_folder, row['folder'], 'output', 'mat_data.csv')
    if os.path.exists(fp_prices):

        # df_mat_data = pd.read_csv(fp_prices, header = [0,1], index_col=0)
        df_mat_data = read_pint_df(fp_prices)
        
        #Custom data dataset already has source column
        if 'source' in df_mat_data.columns:
            for sub_source in df_mat_data['source']:
                price_sources.append(sub_source)
                price_folders.append(row['folder'])
        else:
            price_sources.append(source)
            price_folders.append(row['folder'])

            df_mat_data['source'] = source

        # if 'pub' in row['folder']:
        #     df_mat_data['type'] = 'Publication'
        # else:
        #     df_mat_data['type'] = '-'

        dfs_mat_data.append(df_mat_data)



df_mat_data = pd.concat(dfs_mat_data)
# %%

# price_source_type_lookup = pd.Series(price_folders, index=price_sources)
# price_source_type_lookup.name = 'folder'
# price_source_type_lookup.to_csv('price_source_type_lookup.csv')

#%%

price_source_type_lookup = pd.read_csv('price_source_type_lookup.csv', index_col=0)

price_source_type_lookup



#%%

df_price_source = df_mat_data[['specific_price','source']]
df_price_source['specific_price']  = df_price_source['specific_price'].pint.to('USD/kg').pint.magnitude

#%%


types = [price_source_type_lookup.loc[s,'type'] for s in df_price_source['source']]

df_price_source['type'] = types


df_price_type = df_price_source[['specific_price','type']].set_index('type',append=True)#

df_price_type

# %%

price_avg = df_price_type.groupby('index').mean()['specific_price']
price_avg.name = 'specific_price_all'

price_avg


# specific_price_mag = df_price_source['specific_price'].pint.to('USD/kg').pint.magnitude
# specific_price_mag.groupby('index').median()


#%%

price_type_avg = df_price_type.groupby(['index','type']).mean()

price_type_avg = price_type_avg.reset_index()

price_type_avg

#%%

df_together = pd.merge(price_type_avg, price_avg, on='index')


df_together['diff'] = df_together['specific_price'] - df_together['specific_price_all']
df_together['rat'] = df_together['specific_price']/df_together['specific_price_all']

df_together['rat']

df_together.groupby('type')['rat'].mean()
# df_together.groupby('type')['diff'].std()

#%%

df_together.groupby('type')['rat'].hist(legend=True)

# plt.legend()




# %%
