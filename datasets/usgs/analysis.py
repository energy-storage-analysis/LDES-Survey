import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %%
bins = np.logspace(np.log10(0.1), np.log10(1e6), 50)
df['price_per_kg'].hist(bins=bins)
plt.xscale('log')

#%%



#%%
df_high = df.where(df['price_per_kg'] >1e3).dropna()
df_high[['Commodity','price_per_kg']].sort_values('price_per_kg')
#%%
df_low = df.where(df['price_per_kg'] <10).dropna()
df_low.sort_values('price_per_kg').iloc[0:50]
# %%
avg_price = df.groupby('Commodity')['price_per_kg'].mean()
avg_price = avg_price.sort_values()
avg_price.name = 'average_price'
avg_price.iloc[0:50]

# %%
bins = np.logspace(np.log10(0.1), np.log10(1e6), 50)
avg_price.hist(bins=bins)
plt.xscale('log')
plt.xlabel('Cost ($/kg)')
plt.ylabel('Count')

#%%
std_price = df.groupby('Commodity')['price_per_kg'].std()
std_price = std_price.sort_values()
std_price.name = 'stddev_price'
# %%
commodity_counts = df['Commodity'].sort_values(ascending=False).value_counts()
commodity_counts.name = 'num_entries'

df_commodity = pd.concat([
    df['Commodity'],
    commodity_counts,
    avg_price,
    std_price 
], axis=1)
df_commodity

#%%

df_commodity['ratio'] = df_commodity['stddev_price']/df_commodity['average_price']

df_commodity.sort_values('ratio', ascending=False)