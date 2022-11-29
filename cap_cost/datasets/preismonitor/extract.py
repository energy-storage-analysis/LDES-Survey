#%%

import pandas as pd

df = pd.read_csv('input.csv', index_col=0)


# %%
df['price'] = df['price'].str.replace(r'.', '', regex=False).str.replace(',', '.')

df['price'] = df['price'].astype(float)
# %%

df['price_unit'] = df['price_unit'].str.replace(r'US$', 'USD', regex=False)
df['price_unit'] = df['price_unit'].str.replace(r'€', 'EUR', regex=False)
df['price_unit'] = df['price_unit'].str.replace('dmtu', 'metric_ton') 
df['price_unit'] = df['price_unit'].str.replace('mtu', 'metric_ton') 
df['price_unit'] = df['price_unit'].str.replace('troz', 'troy_ounce') 
df['price_unit'] = df['price_unit'].str.replace('RMB', 'CNY') 
# df['price_unit'] = df['price_unit'].str.replace('US$', 'USD')


df['price_unit'].value_counts()
# %%

df.to_csv('output/extracted.csv')
# %%
