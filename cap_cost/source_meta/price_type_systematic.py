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


from es_utils.cpi import get_cpi_data
cpi_data = get_cpi_data()
dataset_years = pd.read_csv(pjoin(dataset_folder,'dataset_years.csv'), index_col=0)['year'].dropna()

dfs_mat_data = []

price_sources = []
price_folders = []

# TODO: Why can't I just read mat data?  or refactor this with consolidate data
# Not correcteed for inflation

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

        if 'year' not in df_mat_data.columns:
            if source not in dataset_years.index:
                raise ValueError("Did not find a year for mat data source: {}".format(source))
            else:
                df_mat_data['year'] = dataset_years[source]


        # if 'pub' in row['folder']:
        #     df_mat_data['type'] = 'Publication'
        # else:
        #     df_mat_data['type'] = '-'

        dfs_mat_data.append(df_mat_data)



df_mat_data = pd.concat(dfs_mat_data)

df_mat_data['specific_price'] = df_mat_data['specific_price']*df_mat_data['year'].map(cpi_data)

# %%

# price_source_type_lookup = pd.Series(price_folders, index=price_sources)
# price_source_type_lookup.name = 'folder'
# price_source_type_lookup.to_csv('price_source_type_lookup.csv')

#%%

df_mat_data_final = read_pint_df(pjoin(REPO_DIR, 'cap_cost/data_consolidated/mat_data.csv'), index_col=0, drop_units=True)
# df_mat_data_final 
df_mat_data_used = df_mat_data_final.where(df_mat_data_final['num_SMs'] > 0).dropna(how='all')
df_mat_data_used 
# df_mat_data_used

# df_mat_data_final.index

#%%

#TODO: Check and make stats. only keep used final mat prices
df_mat_data = df_mat_data.loc[df_mat_data_used.index]


#%%

price_source_type_lookup = pd.read_csv('price_source_type_lookup.csv', index_col=0)

# price_source_type_lookup['type'] = price_source_type_lookup['type'] +' ' + price_source_type_lookup['type2']
price_source_type_lookup['type'] =  price_source_type_lookup['type2']

price_source_type_lookup



#%%

df_price_source = df_mat_data[['specific_price','source']]
df_price_source['specific_price']  = df_price_source['specific_price'].pint.to('USD/kg').pint.magnitude

#%%

types = [price_source_type_lookup.loc[s,'type'] for s in df_price_source['source']]

df_price_source['type'] = types

df_price_type = df_price_source[['specific_price','type']].set_index('type',append=True)#

df_price_type

#%%

fig,axes = plt.subplots(1,2, figsize=(5,4))

price_source_type_lookup['type'].value_counts().plot.bar(ax=axes[0])

axes[0].set_ylabel("Source Counts")

df_price_source['type'].value_counts().plot.bar(ax=axes[1])


axes[1].set_ylabel("Price Datapoint Counts")

fig.tight_layout()

# %%

price_avg = df_price_type.groupby('index').median()['specific_price']
price_avg.name = 'specific_price_all'

price_avg

# specific_price_mag = df_price_source['specific_price'].pint.to('USD/kg').pint.magnitude
# specific_price_mag.groupby('index').median()

#%%

price_type_avg = df_price_type.groupby(['index','type']).median()

#%%

df_together = pd.merge(price_type_avg.reset_index('type'), price_avg, on='index')

df_together = df_together.drop('Air')

# Add noise to investigate if there is an effect from prices being presented with limited significant digits
# df_together['specific_price'] = df_together['specific_price'] + np.random.random(len(df_together))*0.01

df_together


#%%
df_together['diff'] = df_together['specific_price'] - df_together['specific_price_all']
df_together['rat'] = df_together['specific_price']/df_together['specific_price_all']
df_together['diff_frac'] = abs(df_together['diff'])/df_together['specific_price_all']

# df_together['diff_frac'].hist()
# df_together.loc['Li2S']

#%%


df_together.sort_values(by='diff_frac').dropna().iloc[0:10]
# df_together.sort_values(by='diff_frac').dropna().iloc[-10:-1]

#%%


df2 = df_together.where(df_together['rat'] != 1.0).dropna(how='all')

rat_min = df2['rat'].min()*0.9
rat_max = df2['rat'].max()*1.1

import numpy as np
bins = np.logspace(np.log10(rat_min), np.log10(rat_max), 50)


df2.groupby('type')['rat'].hist(legend=True, bins=bins)
plt.xscale('log')

#%%

df2 = df_together.where(df_together['diff_frac'] != 0).dropna(how='all')

rat_min = df2['diff_frac'].min()*0.9
rat_max = df2['diff_frac'].max()*1.1

bins = np.logspace(np.log10(rat_min), np.log10(rat_max), 50)


df2.groupby('type')['diff_frac'].hist(legend=True, bins=bins)
plt.xscale('log')

# plt.legend()

#%%

fig, axes = plt.subplots(4, sharex=True, sharey=True, figsize= (5,5))

for i, source_type in enumerate(set(df2['type'])):
    df_sel = df2.where(df2['type'] == source_type).dropna(how='all')

    df_sel['rat'].plot.hist(ax = axes[i], bins=bins)
    axes[i].set_xscale('log')
    axes[i].set_ylabel('Counts\n{}'.format(source_type))


# axes[-1].set_xlabel("Ratio of individual price to overall price median")
# plt.xscale('log')

# %%

print("Price ratio of specific source to overall median: ")

print("Median of all ratios: ")

print(df2.groupby('type')['rat'].median())


print("Mean of all ratios: ")
print(df2.groupby('type')['rat'].mean())
# %%
