import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %%
bins = np.logspace(np.log10(0.1), np.log10(1e6), 50)
df['specific_price'].hist(bins=bins)
plt.xscale('log')

#%%



#%%
df_high = df.where(df['specific_price'] >1e3).dropna()
df_high[['Commodity','specific_price']].sort_values('specific_price')
#%%
df_low = df.where(df['specific_price'] <10).dropna()
df_low.sort_values('specific_price').iloc[0:50]
# %%
avg_price = df.groupby('Commodity')['specific_price'].mean()
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
std_price = df.groupby('Commodity')['specific_price'].std()
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