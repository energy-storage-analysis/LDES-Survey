#%%

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
df = pd.read_csv('data/prices.csv', index_col=0)
# df = df.iloc[0:20]
df = df.dropna(subset=['price'])
df


#Factor to convert to $/kg
kg_per_lb = 0.454
kg_per_oz = 0.0283495
kg_per_toz = 0.0311035
kg_per_st = 907.185
kg_per_flask = 34.47
kg_per_carat = 0.0002
d_per_cents = 0.01

factors = {
    'ctslb': d_per_cents/kg_per_lb ,
    'dlb': 1/kg_per_lb,
    'dkg': 1,
    'kg': 1,
    'dt': 1/1000,
    'dst': 1/kg_per_st,
    'dlb': 1/kg_per_lb,
    'dct': 1/kg_per_carat,
    'Index':  10, #??  Consumer price index
    't': 1/1000 , 
    'df': 1/kg_per_flask, 
    'dto': 1/kg_per_toz, 
    'dtoz': 1/kg_per_toz,
    'dg': 1000
}

factor_values = [factors[unit] for unit in df['price_units']]
# factor_values

# %%
df['price_kg'] = df['price']*factor_values
df['price_kg']
# %%
bins = np.logspace(np.log10(0.1), np.log10(1e6), 50)
df['price_kg'].hist(bins=bins)
plt.xscale('log')

#%%
df_high = df.where(df['price_kg'] >1e3).dropna()
df_high[['Commodity','price_kg']].sort_values('price_kg')
#%%
df_low = df.where(df['price_kg'] <10).dropna()
df_low.sort_values('price_kg').iloc[0:50]
# %%
avg_price = df.groupby('Commodity')['price_kg'].mean()
avg_price = avg_price.sort_values()
avg_price

#%%
avg_price.iloc[0:50]
# %%
bins = np.logspace(np.log10(0.1), np.log10(1e6), 50)
avg_price.hist(bins=bins)
plt.xscale('log')
plt.xlabel('Cost ($/kg)')
plt.ylabel('Count')