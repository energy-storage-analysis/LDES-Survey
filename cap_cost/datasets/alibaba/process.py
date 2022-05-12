#%%
import pandas as pd

df = pd.read_csv('output/extracted.csv', index_col=0)

df = df.dropna(subset=['keep']) #Get rid of manually dropped entries

price_use = df['scaled_anhydrous_price'].fillna(df['specific_price'])
df['specific_price'] = price_use

#%%
df_t = df.dropna(how='all')



#%%

df_stats = df_t.reset_index().groupby('index').agg({'specific_price':['median', 'std','count']})['specific_price']


df_stats['ratio'] = df_stats['std']/df_stats['median']
df_stats

#%%

df_prices = df_stats[['median', 'std','ratio','count']]

# index_lookup = df_t.reset_index()[['index', 'search_text']].groupby('search_text')['index'].first()

# df_prices['index'] = [index_lookup[f] for f in df_prices.index]

# df_prices = df_prices.reset_index().set_index('index')

df_prices.to_csv('output/processed.csv')

df_mat_data = df_prices[['median']].rename({'median':'specific_price'}, axis=1)


#%%
search_table = pd.read_csv(r'scrapy_alibaba\resources\mat_data_searches.csv', index_col=0)

search_table = search_table[~search_table.index.duplicated()]


df_mat_data = pd.merge(df_mat_data.reset_index(), search_table[['molecular_formula']].reset_index())

df_mat_data = df_mat_data.set_index('index')
# df_mat_data['molecular_formula'] = search_table.loc[df_mat_data.index]['molecular_formula']

#%%

df_mat_data.to_csv('output/mat_data.csv')

# %%
