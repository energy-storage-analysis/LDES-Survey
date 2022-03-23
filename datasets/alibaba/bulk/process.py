import pandas as pd

df = pd.read_csv('output/extracted.csv', index_col=0)

search_lookup = pd.read_csv('keywords_bulk.csv').set_index('search_text')[['index', 'molecular_formula']]


df_t = df.where((df['min_quantity_kg'] > 99)).dropna(how='all')


df_t.index.value_counts()
#%%

df_stats = df_t.reset_index().groupby('search_text').agg({'specific_price':['mean', 'std','count']})['specific_price']


df_stats['ratio'] = df_stats['std']/df_stats['mean']
df_stats

#%%

df_prices = df_stats[['mean']].rename({'mean':'specific_price'}, axis=1)

# df_prices['original_name'] = df_stats.index

# df_prices = df_prices.reset_index()

# df_prices['index'] = df_t.groupby('search_term').first()['index']
df_prices['index'] = [search_lookup['index'][f] for f in df_prices.index]
df_prices['molecular_formula'] = [search_lookup['molecular_formula'][f] for f in df_prices.index]

df_prices


#%%

df_prices = df_prices.set_index('index')

df_prices
#%%


df_prices.to_csv('output/mat_data.csv')

# %%
