#%%

import pandas as pd


df = pd.read_csv('output/extracted.csv', index_col=0)

# df = df.where(df['min_quantity_kg'] >= 1).dropna(how='all')
df
# %%

#%%
df_t = df.dropna(how='all')
df_stats = df_t.reset_index().groupby('index').agg({'specific_price':['median', 'std','count']})['specific_price']
df_stats['ratio'] = df_stats['std']/df_stats['median']

#%%
df_prices = df_stats[['median', 'std','ratio','count']]
df_prices.to_csv('output/processed.csv')
df_mat_data = df_prices[['median']].rename({'median':'specific_price'}, axis=1)

# df_price = df.groupby('index')['specific_price'].mean()
# %%

from es_utils.units import prep_df_pint_out

df_mat_data = df_mat_data.astype({
    'specific_price': 'pint[USD/kg]'
})

df_mat_data = prep_df_pint_out(df_mat_data)

df_mat_data.to_csv('output/mat_data.csv')
# %%
