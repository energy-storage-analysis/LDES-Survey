#%%
import pandas as pd
from es_utils.units import convert_units, prep_df_pint_out, ureg

df = pd.read_csv('output/extracted.csv', index_col=0)
df = df.dropna(subset=['keep']) #Get rid of manually dropped entries
df = df[df['specific_price'] != 0.001] # Drop prices that are exactly 0.001 $/kg, vendors seem to do this for visibility

price_use = df['scaled_anhydrous_price'].fillna(df['specific_price'])
df['specific_price'] = price_use

#%%
df_t = df.dropna(how='all')
df_stats = df_t.reset_index().groupby('index').agg({'specific_price':['median', 'std','count']})['specific_price']
df_stats['ratio'] = df_stats['std']/df_stats['median']

#%%
df_prices = df_stats[['median', 'std','ratio','count']]
df_prices.to_csv('output/processed.csv')
df_mat_data = df_prices[['median']].rename({'median':'specific_price'}, axis=1)

#%%
#Merge with the original search table to get the molecular formulas. Probably a better way to do this. 

search_table = pd.read_csv(r'scrapy_alibaba\resources\mat_data_searches.csv', index_col=0)
search_table = search_table[~search_table.index.duplicated()]

df_mat_data = pd.merge(df_mat_data.reset_index(), search_table[['molecular_formula']].reset_index(), how='outer')
df_mat_data = df_mat_data.set_index('index')
df_mat_data = df_mat_data.dropna(subset=['specific_price'])

#%%



df_mat_data = df_mat_data.astype({
    'specific_price': 'pint[USD/kg]'
})

df_mat_data = prep_df_pint_out(df_mat_data)

df_mat_data.to_csv('output/mat_data.csv')

# %%
