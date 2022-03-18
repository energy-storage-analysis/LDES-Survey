#%%
#%%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



import seaborn as sns

df = pd.read_csv('output/processed.csv', index_col=0)

sns.scatterplot(data=df, x='min_quantity_kg', y='specific_price')
plt.xscale('log')
plt.yscale('log')


# %%
df.index.value_counts()
#%%

df_t = df.where(df['min_quantity_kg'] > 999).dropna(how='all')

df_t.index.value_counts()
#%%

df_stats = df_t.reset_index().groupby('index').agg({'specific_price':['mean', 'std','count']})['specific_price']


df_stats['ratio'] = df_stats['std']/df_stats['mean']
df_stats['original_name'] = df_t.groupby('index').first()['search_text']
df_stats



# %%
df_stats.sort_values('mean')

#%%

df_stats.sort_values('ratio', ascending=False)

#%%

df_prices = df_stats[['mean','original_name']].rename({'mean':'specific_price'}, axis=1)
df_prices.to_csv('output/mat_prices.csv')

#%%

df_t.loc['NiO4S']#['specific_price']
# %%

# %%
