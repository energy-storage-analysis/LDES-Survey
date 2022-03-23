#%%
import pandas as pd

df = pd.read_csv('output/extracted_edit.csv', index_col=0)
df
#%%
df_single = pd.read_csv('single_manual.csv', index_col=0)
isin_single = pd.Series(df.index.isin(df_single.index), index=df.index)

df_t = df.where((df['min_quantity_kg'] > 99) | isin_single).dropna(how='all')

search_lookup = df_t[['index', 'molecular_formula']]
search_lookup = search_lookup.groupby(level=0).first()


search_lookup
#%%

df_stats = df_t.reset_index().groupby('search_text').agg({'specific_price':['mean', 'std','count']})['specific_price']


df_stats['ratio'] = df_stats['std']/df_stats['mean']
df_stats

#%%

df_prices = df_stats[['mean']].rename({'mean':'specific_price'}, axis=1)

# df_prices['original_name'] = df_t.groupby('index').first()['search_text']

df_prices['index'] = [search_lookup['index'][f] for f in df_prices.index]
df_prices['molecular_formula'] = [search_lookup['molecular_formula'][f] for f in df_prices.index]

df_prices = df_prices.set_index('index')

# df_prices['molecular_formula'] = [search_lookup['molecular_formula'][f] for f in df_prices.index]
# df_prices['molecular_formula'] = df_t.groupby('index').first()['molecular_formula']
# df_prices['molecular_formula'] = df_prices.index

df_prices.to_csv('output/mat_data.csv')

# %%
