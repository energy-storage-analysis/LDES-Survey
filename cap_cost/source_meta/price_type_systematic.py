#%%

# make lookup 

#%%
import pandas as pd
from es_utils.units import read_pint_df

import matplotlib.pyplot as plt

import os
from os.path import join as pjoin

#%%

#%%

price_source_type_lookup = pd.read_csv('price_source_type_lookup.csv', index_col=0)

# price_source_type_lookup['type'] = price_source_type_lookup['type'] +' ' + price_source_type_lookup['type2']
price_source_type_lookup['type'] =  price_source_type_lookup['type2']


# price_source_type_lookup

price_source_type_lookup['type'] = price_source_type_lookup['type'].replace({
    'Government': 'Government Agency',
    'Analyst': 'Commodity Analyst',
    'Scientific': 'Scientific Publication',
    'Vendor': 'Vendor'
})

#%%

from es_utils import join_col_vals

type_list = price_source_type_lookup.reset_index().groupby('type')['index'].apply(join_col_vals)

type_list.to_csv('tables/source_type_list.csv')



# %%

figure_output_dir = 'figures/dataset_error'
if not os.path.exists(figure_output_dir): os.mkdir(figure_output_dir)


output_dir = 'tables/dataset_error'
if not os.path.exists(output_dir): os.mkdir(output_dir)


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

# TODO: Not including volumetric prices...Mass density defined for SM. Just copy over volumetric price as we are ultimately just looking at ratios?
df_mat_data_used = df_mat_data_used.dropna(subset=['specific_price'])

df_mat_data_used 
# df_mat_data_used

# df_mat_data_final.index

#%%

table_std_rat = df_mat_data_used.sort_values(by='specific_price_rat', ascending=False).iloc[:20]
table_std_rat = table_std_rat[['specific_price','specific_price_std','specific_price_rat', 'sources','specific_prices']]

table_std_rat.to_csv(os.path.join(output_dir,'tables_std_rat.csv'))

#%%

#TODO: Check and make stats. only keep used final mat prices
df_mat_data = df_mat_data.loc[df_mat_data_used.index]



#%%

df_price_source = df_mat_data[['specific_price','source']]
df_price_source['specific_price']  = df_price_source['specific_price'].pint.to('USD/kg').pint.magnitude

types = [price_source_type_lookup.loc[s,'type'] for s in df_price_source['source']]

df_price_source['type'] = types


#%%

fig,axes = plt.subplots(1,2, figsize=(5,4))

price_source_type_lookup['type'].value_counts().plot.bar(ax=axes[0])

axes[0].set_ylabel("Source Counts")

df_price_source['type'].value_counts().plot.bar(ax=axes[1])


axes[1].set_ylabel("Price Datapoint Counts")

fig.tight_layout()

plt.savefig('figures\price_source_counts.png')

# %%

price_avg = df_price_source['specific_price'].groupby('index').median()

price_avg.name = 'specific_price_all'

price_avg

# specific_price_mag = df_price_source['specific_price'].pint.to('USD/kg').pint.magnitude
# specific_price_mag.groupby('index').median()

#%%

df_price_source2 = df_price_source[['specific_price','source']].set_index('source',append=True)#

price_source_avg = df_price_source2.groupby(['index','source']).median()

price_source_avg = price_source_avg.reset_index('source')

# Having to repeat this....
types = [price_source_type_lookup.loc[s,'type'] for s in price_source_avg['source']]
price_source_avg['type'] = types 

price_source_avg

#%%

df_together = pd.merge(price_source_avg, price_avg, on='index')


# Add noise to investigate if there is an effect from prices being presented with limited significant digits
# df_together['specific_price'] = df_together['specific_price'] + np.random.random(len(df_together))*0.01

df_together['diff'] = df_together['specific_price'] - df_together['specific_price_all']

# We keep only prices with nonzero difference from overall median. Note this also includes individual prices that are e.g. in the middle of three prices. 
print("Length with all prices: {}".format(len(df_together)))
df_together_equal = df_together.where(df_together['diff'] == 0).dropna(how='all')
df_together = df_together.where(df_together['diff'] != 0).dropna(how='all')
print("Length after removing prices equal to overall median: {}".format(len(df_together)))


## Used to confirm that all mat data with only one source (see figure 3) are in the removed dataset. 
# one_source = df_mat_data_used.where(df_mat_data_used['num_source'] == 1).dropna(how='all')
# df_together_equal.loc[one_source.index]

# df_together = df_together.drop('Air')


df_together['rat'] = df_together['specific_price']/df_together['specific_price_all']
df_together['diff_frac'] = abs(df_together['diff'])/df_together['specific_price_all']

#%%

df_together[['source_list','source_list_prices']] = df_mat_data_final.loc[df_together.index][['sources','specific_prices']]

df_out = df_together[['source','specific_price','specific_price_all','rat','diff_frac','source_list','source_list_prices']]

table_diff_frac_high = df_out.sort_values(by='diff_frac', ascending=False).dropna().iloc[:20]
table_diff_frac_high.to_csv(os.path.join(output_dir,'diff_frac_high.csv'))


table_rat_indiv_high = df_out.sort_values(by='rat', ascending=False).dropna().iloc[:20]
table_rat_indiv_high.to_csv(os.path.join(output_dir,'rat_indiv_high.csv'))


table_rat_indiv_low = df_out.sort_values(by='rat', ascending=True).dropna().iloc[:20]
table_rat_indiv_low.to_csv(os.path.join(output_dir,'rat_indiv_low.csv'))

#%%

plt.figure()

rat_min = df_together['rat'].min()*0.9
rat_max = df_together['rat'].max()*1.1

import numpy as np
bins = np.logspace(np.log10(rat_min), np.log10(rat_max), 50)


df_together.groupby('type')['rat'].hist(legend=True, bins=bins)
plt.xscale('log')

plt.suptitle('Ratio of individual price to overall price median')
plt.savefig(os.path.join(figure_output_dir, 'ratio_all.png'))


#%%


fig, axes = plt.subplots(4, sharex=True, sharey=True, figsize= (5,5))

for i, source_type in enumerate(set(df_together['type'])):
    df_sel = df_together.where(df_together['type'] == source_type).dropna(how='all')

    df_sel['rat'].plot.hist(ax = axes[i], bins=bins)
    axes[i].set_xscale('log')
    axes[i].set_ylabel('{}'.format(source_type.replace(" ", "\n")))


axes[-1].set_xlabel("(Individual Price)/(Price Median)")
# plt.xscale('log')

plt.savefig(os.path.join(figure_output_dir, 'ratio_separate.png'))

#%%

plt.figure()

rat_min = df_together['diff_frac'].min()*0.9
rat_max = df_together['diff_frac'].max()*1.1

bins = np.logspace(np.log10(rat_min), np.log10(rat_max), 50)


df_together.groupby('type')['diff_frac'].hist(legend=True, bins=bins)
plt.xscale('log')

# plt.legend()


plt.suptitle('(Individual price - price median)/price_median')
plt.savefig(os.path.join(figure_output_dir, 'diff_frac_all.png'))

#%%

fig, axes = plt.subplots(4, sharex=True, sharey=True, figsize= (5,5))

for i, source_type in enumerate(set(df_together['type'])):
    df_sel = df_together.where(df_together['type'] == source_type).dropna(how='all')

    df_sel['diff_frac'].plot.hist(ax = axes[i], bins=bins)
    axes[i].set_xscale('log')
    axes[i].set_ylabel('{}'.format(source_type.replace(" ", "\n")))


axes[-1].set_xlabel("|Individual price - Price median|/(Price Median)")
# plt.xscale('log')

plt.savefig(os.path.join(figure_output_dir, 'diff_frac_separate.png'))

# %%

# Stats

rat_median = df_together.groupby('type')['rat'].median()
rat_median.name = 'ratio_median'
rat_mean = df_together.groupby('type')['rat'].mean()
rat_mean.name = 'ratio_mean'

diff_frac_median = df_together.groupby('type')['diff_frac'].median()
diff_frac_median.name = 'diff_frac_median'
diff_frac_mean = df_together.groupby('type')['diff_frac'].mean()
diff_frac_mean.name = 'diff_frac_mean'

rat_median
df_stats = pd.concat([rat_median,rat_mean,diff_frac_median, diff_frac_mean],axis=1)


df_stats.to_csv(os.path.join(output_dir, 'error_stats.csv'))
# %%
